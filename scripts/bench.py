#!/usr/bin/env python3
import argparse
from copy import copy
from jinja2 import Environment, FileSystemLoader
import math
import os
import shutil
import subprocess

import ashes
import dota
from utils import *
import vulkan_sponza

games = [dota, ashes, vulkan_sponza]

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
		for per_wave in [False]:
			for late in [True, False]:
				config = RunConfig(gen=gen, use=not gen, per_wave=per_wave, late=late, uniform=True)
				sig = config.get_signature()
				print(f"\n\nRunning {sig}")
				try:
					run_game(args.game, config, debug=args.debug)
				except:
					print("Error running game")
					pass

				# Save pipelines
				orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
				pipe_folder = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
				shutil.rmtree(pipe_folder, ignore_errors=True)
				os.rename(orig_pipe_folder, pipe_folder)

def bench(args):
	"""Benchmark a game with different PGO options to compare the compiled output"""
	configs = [RunConfig(), RunConfig(use=True, per_wave=True, late=True, uniform=True)]

	config = RunConfig(gen=True, per_wave=True, late=True, uniform=True)
	sig = config.get_signature()
	print(f"\n\nRunning {sig}")
	run_game(args.game, config, debug=args.debug)

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
	config = RunConfig(gen=True, per_wave=True, late=True)
	sig = config.get_signature()
	print(f"\n\nRunning {sig}")
	# run_game(args.game, config, debug=args.debug)

	config = RunConfig(use=True, per_wave=True, late=True, analysis=True)
	sig = config.get_signature()
	analysis_file = "/tmp/mydriveranalysis.txt"
	if os.path.isfile(analysis_file):
		os.remove(analysis_file)

	print(f"\n\nAnalyzing {sig}")
	run_game(args.game, config, debug=args.debug)

	shaders = []
	with open(analysis_file) as f:
		first = True
		for l in f:
			l = l.strip()
			if l == "Compiling":
				if not first:
					shaders.append((zero, total))
				else:
					first = False

				zero = 0
				total = 0
			elif l == "Count is 0":
				zero += 1
				total += 1
			elif l.startswith("Count is "):
				total += 1
			elif len(l) != 0:
				raise Exception(f"Unknown line '{l}'")

		if not first:
			shaders.append((zero, total))

	print(f"Shaders: {shaders}")

def main():
	actions = {
		"diff": diff,
		"bench": bench,
		"analysis": analysis,
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
