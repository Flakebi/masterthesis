#!/usr/bin/env python3
import argparse
from copy import copy
from jinja2 import Environment, FileSystemLoader
import math
import os
from os import listdir
from os.path import isfile, join
import shutil
import subprocess

import ashes
import dota
import switch_vm
import test_uniform
from utils import *
import vulkan_sponza

games = [dota, ashes, vulkan_sponza, switch_vm, test_uniform]

def run_game(name, config, remove_cache=True, debug=False):
	if (not config.gen and not config.use) and (config.per_wave or config.late or config.uniform or config.analysis):
		print("WARNING PGO options have no meaning when PGO is not in use")

	sig = config.get_signature()
	env = dict(os.environ)
	env["VK_ICD_FILENAMES"] = "/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json"
	pgo_config = copy(config)
	pgo_config.gen = False
	pgo_config.use = False
	pgo_sig = pgo_config.get_signature()
	pgo_folder = f"/home/sebi/Downloads/pgo/{name}-{pgo_sig}"
	if config.gen:
		# Remove pgo folder and recreate
		shutil.rmtree(pgo_folder, ignore_errors=True)
		#os.makedirs(pgo_folder, exist_ok=True)
		os.makedirs(pgo_folder)
		env["AMDVLK_PROFILE_INSTR_GEN"] = f"{pgo_folder}/Pipeline_%i_%m.profraw"
	if config.use:
		env["AMDVLK_PROFILE_INSTR_USE"] = f"{pgo_folder}/Pipeline_%i.profdata"
	if config.per_wave:
		env["AMDVLK_PROFILE_PER_WAVE"] = "1"
	if config.late:
		env["AMDVLK_PROFILE_LATE"] = "1"
	if config.uniform:
		env["AMDVLK_PROFILE_UNIFORM"] = "1"
	if config.analysis:
		env["AMDVLK_PROFILE_ANALYSIS"] = "1"
	if config.remove:
		env["AMDVLK_PROFILE_REMOVE"] = "1"

	if name == "test":
		subprocess.run("env", check=True, env=env, shell=True)
		result = None
	else:
		game_found = False
		for g in games:
			if g.name == name:
				result = g.run(env, remove_cache, debug, sig)
				game_found = True
		if not game_found:
			raise Exception(f"Unknown game '{name}'")

	if config.gen:
		# Convert pgo data
		subprocess.run("/home/sebi/Masterarbeit/repo/scripts/convert_pipelines.sh", check=True, env=env, cwd=pgo_folder)

	return result

def setup():
	subprocess.run("echo profile_standard > /sys/class/drm/card0/device/power_dpm_force_performance_level", check=True, shell=True)
	subprocess.run("for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $f; done", check=True, shell=True)
	subprocess.run("echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo", check=True, shell=True)
	# Turn fan up, 255 is 100%
	subprocess.run("echo 1 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_enable", check=True, shell=True)
	subprocess.run("echo 120 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1", check=True, shell=True)

def teardown():
	subprocess.run("echo auto > /sys/class/drm/card0/device/power_dpm_force_performance_level", check=True, shell=True)
	subprocess.run("for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo powersave > $f; done", check=True, shell=True)
	subprocess.run("echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo", check=True, shell=True)
	# Fan to auto
	subprocess.run("echo 2 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_enable", check=True, shell=True)
	pass

def extract(line, key):
	if key in line:
		p0 = line.rfind('x') + 1
		return int(line[p0:], 16)
	return None

def registers(args):
	configs = [
		RunConfig(),
		RunConfig(gen=True, per_wave=True, late=True, remove=True),
		RunConfig(use=True, per_wave=True, late=True, remove=True),
	]

	registers = {}
	for config in configs:
		rs = []
		sig = config.get_signature()
		path = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
		files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".pipe")]
		for file in files:
			vs_vgprs = 0
			vs_sgprs = 0
			ps_vgprs = 0
			ps_sgprs = 0
			with open(join(path, file), "r") as f:
				for l in f:
					r = extract(l, "VS_NUM_USED_VGPRS")
					if r is not None:
						vs_vgprs = r
					r = extract(l, "VS_NUM_USED_SGPRS")
					if r is not None:
						vs_sgprs = r
					r = extract(l, "PS_NUM_USED_VGPRS")
					if r is not None:
						ps_vgprs = r
					r = extract(l, "PS_NUM_USED_SGPRS")
					if r is not None:
						ps_sgprs = r

			if vs_vgprs == 0 and ps_vgprs == 0:
				continue
			rs.append([vs_vgprs, vs_sgprs, ps_vgprs, ps_sgprs])
			# print(f"{file}\nVS vgprs: {vs_vgprs}\n   sgprs: {vs_sgprs}\nPS vgprs: {ps_vgprs}\n   sgprs: {ps_sgprs}\n")

		# Compute average
		sums = [sum(r) / len(rs) for r in zip(*rs)]
		print(f"{sig}: {sums}")

		registers[config] = rs
		# print("")

def diff(args):
	"""Run a game with different PGO options to compare the compiled output"""
	config = RunConfig()
	sig = config.get_signature()
	print(f"\n\nRunning {sig}")
	try:
		run_game(args.game, config, debug=args.debug)
	except:
		pass

	# Save pipelines
	orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
	pipe_folder = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
	shutil.rmtree(pipe_folder, ignore_errors=True)
	os.rename(orig_pipe_folder, pipe_folder)

	for gen in [True, False]:
		for uniform in [False, True]:
			config = RunConfig(gen=gen, use=not gen, late=True, uniform=uniform)
			sig = config.get_signature()
			print(f"\n\nRunning {sig}")
			# try:
			run_game(args.game, config, debug=args.debug)
			# except:
				# print("Error running game")
				# pass

			# Save pipelines
			orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
			pipe_folder = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
			shutil.rmtree(pipe_folder, ignore_errors=True)
			os.rename(orig_pipe_folder, pipe_folder)

def bench(args):
	"""Benchmark a game with different PGO options to compare the compiled output"""
	configs = [RunConfig(), RunConfig(use=True, late=True, uniform=True)]

	config = RunConfig(gen=True, late=True, uniform=True)
	sig = config.get_signature()
	print(f"\n\nRunning {sig}")
	# run_game(args.game, config, debug=args.debug)

	results = {}
	for config in configs:
		results[config] = []

	count = 3
	for i in range(count):
		for config in configs:
			sig = config.get_signature()
			print(f"\n\nRunning {sig} {i + 1}/{count}")
			r = run_game(args.game, config, remove_cache=(i == 0), debug=args.debug)
			results[config].append(r)

	print(f"\nResults:")
	tmpl_results = []
	for config, res in results.items():
		times = [r.frame_time for r in res]
		avg_time = avg(times)

		if len(times) > 1:
			time_dev = deviationStudentT(times)
		else:
			time_dev = 0
		print(f"{config.get_signature()}: {times}\n\t({avg(times) * 1000} ± {time_dev * 1000}) ms")

		times = [t * 1000 for t in times]
		tmpl_results.append((config.get_signature(), avg(times), ":".join([str(t) for t in times])))

	env = Environment(loader=FileSystemLoader(""))
	template = env.get_template("composite.xml.j2")
	res = template.render(game=args.game, results=tmpl_results)
	with open("composite.xml", "w") as f:
		f.write(res)

def analysis(args):
	"""Run the PGO analyzation pass, this needs existing PGO generated data"""
	config = RunConfig(gen=True, uniform=True, late=True)
	sig = config.get_signature()
	print(f"\n\nRunning {sig}")
	run_game(args.game, config, debug=args.debug)

	config = RunConfig(use=True, uniform=True, late=True, analysis=True)
	sig = config.get_signature()
	analysis_file = "/tmp/mydriveranalysis.txt"
	if os.path.isfile(analysis_file):
		os.remove(analysis_file)

	print(f"\n\nAnalyzing {sig}")
	run_game(args.game, config, debug=args.debug)

	dead_code = []
	uniformity = []
	with open(analysis_file) as f:
		first = True
		for l in f:
			l = l.strip()
			if l == "Compiling":
				if not first:
					dead_code.append((zero, total))
					uniformity.append((uni_static, uni_dynamic, uni_divergent))
				else:
					first = False

				zero = 0
				total = 0

				uni_static = 0
				uni_dynamic = 0
				uni_divergent = 0
			elif l == "Count is 0":
				zero += 1
				total += 1
			elif l.startswith("Count is "):
				total += 1
			elif l.startswith("Static uniform"):
				uni_static += 1
			elif l.startswith("Dynamic uniform"):
				uni_dynamic += 1
			elif l.startswith("Divergent"):
				uni_divergent += 1
			elif len(l) != 0:
				raise Exception(f"Unknown line '{l}'")

		if not first:
			dead_code.append((zero, total))
			uniformity.append((uni_static, uni_dynamic, uni_divergent))

	print(f"Dead code: {dead_code}")
	print(f"Uniformity: {uniformity}")

def main():
	actions = {
		"diff": diff,
		"bench": bench,
		"analysis": analysis,
		"registers": registers,
	}

	parser = argparse.ArgumentParser(description="Benchmarks!")
	parser.add_argument("action", choices=list(actions.keys()) + ["setup", "teardown"])
	game_names = [g.name for g in games]
	parser.add_argument("-g", "--game", choices=game_names + ["test"])
	parser.add_argument("-d", "--debug", help="Start in a debugger")

	args = parser.parse_args()

	if args.action in actions:
		actions[args.action](args)
	elif args.action == "setup":
		setup()
	elif args.action == "teardown":
		teardown()
	else:
		raise Exception(f"Unknown action '{action}'")

if __name__ == "__main__":
	main()
