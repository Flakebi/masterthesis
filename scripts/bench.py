#!/usr/bin/env python3
import argparse
from copy import copy
import datetime
from jinja2 import Environment, FileSystemLoader
import math
import os
from os import listdir
from os.path import isfile, join
import shutil
import subprocess

from utils import *

import ashes
import dota
import dow3
import f12017
import infiltrator
import madmax
import switch_vm
import test_uniform
import vulkan_sponza

games = [ashes, dota, dow3, f12017, infiltrator, madmax, switch_vm, test_uniform, vulkan_sponza]

def run_game(name, config, remove_cache=True, debug=False):
	if (not config.gen and not config.use) and (config.per_wave or config.late or config.uniform or config.analysis):
		print("WARNING PGO options have no meaning when PGO is not in use")

	sig = config.get_signature()
	env = {}
	env["VK_ICD_FILENAMES"] = "/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json"
	pgo_config = copy(config)
	pgo_config.gen = False
	pgo_config.use = False
	pgo_config.remove = False
	pgo_config.analysis = False
	pgo_sig = pgo_config.get_signature()
	pgo_folder = f"/home/sebi/Downloads/pgo/{name}-{pgo_sig}"
	if config.gen:
		# Remove pgo folder and recreate
		shutil.rmtree(pgo_folder, ignore_errors=True)
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
	if config.non_atomic:
		env["AMDVLK_PROFILE_NON_ATOMIC"] = "1"

	orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
	shutil.rmtree(orig_pipe_folder, ignore_errors=True)

	game_found = False
	for g in games:
		if g.name == name:

			result = g.run(env, remove_cache, debug, sig)
			game_found = True
	if not game_found:
		raise Exception(f"Unknown game '{name}'")

	# Save pipelines
	pipe_folder = f"/home/sebi/Downloads/Pipelines/{name}-{sig}"
	shutil.rmtree(pipe_folder, ignore_errors=True)
	os.rename(orig_pipe_folder, pipe_folder)

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

def register_diff(a, b):
	return sum([abs(x - y) for x, y in zip(a, b)])

def registers_diff(registers, f):
	diff = 0
	reg_vals = list(registers.values())
	reg0 = reg_vals[0][f]
	for rs in reg_vals[1:]:
		if f in rs:
			diff += register_diff(reg0, rs[f])
	return diff

def open_data():
	f = open("data.py", "a")
	date = datetime.datetime.now()
	f.write(f"\n# {date:%Y-%m-%d %H:%M}\n")
	return f

def registers(args):
	if len(args.config) < 1:
		raise Exception("Please tell me the configs")

	configs = [get_config(c) for c in args.config]

	registers = {}
	for config in configs:
		rs = {}
		sig = config.get_signature()
		path = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
		files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".pipe")]
		for file in files:
			cs_vgprs = 0
			cs_sgprs = 0
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
					r = extract(l, "CS_NUM_USED_VGPRS")
					if r is not None:
						cs_vgprs = r
					r = extract(l, "CS_NUM_USED_SGPRS")
					if r is not None:
						cs_sgprs = r

			if cs_vgprs == 0 and vs_vgprs == 0 and ps_vgprs == 0:
				continue
			rs[file] = [cs_vgprs, cs_sgprs, vs_vgprs, vs_sgprs, ps_vgprs, ps_sgprs]
			# print(f"{file}\nVS vgprs: {vs_vgprs}\n   sgprs: {vs_sgprs}\nPS vgprs: {ps_vgprs}\n   sgprs: {ps_sgprs}\n")

		# Compute average
		rs_vals = rs.values()
		sums = [sum(r) / len(rs_vals) for r in zip(*rs_vals)]
		print(f"{sig}: {sums}")

		registers[config] = rs
		# print("")

	# Sort by difference
	diffs = []
	for f in registers[configs[0]].keys():
		diffs.append((f, registers_diff(registers, f)))

	short_diffs = sorted(diffs, reverse=True, key=lambda d: d[1])

	short_diffs = short_diffs[:min(10, len(short_diffs))]
	for d in short_diffs:
		print(d[0])
		for config in configs:
			sig = config.get_signature()
			print(f"  {sig}: {registers[config][d[0]]}")
		print()

	# Write into file
	with open_data() as f:
		for config in configs:
			sig = config.get_signature()
			f.write(f'registers["{args.game}-{sig}"] = {registers[config]}\n')

def run(args):
	"""Run a game with the supplied PGO options"""
	if len(args.config) < 1:
		raise Exception("Please tell me the configs")

	configs = [get_config(c) for c in args.config]

	for config in configs:
		sig = config.get_signature()
		print(f"\n\nRunning {sig}")
		r = run_game(args.game, config, debug=args.debug)

def bench(args):
	"""Benchmark a game with different PGO options to compare the compiled output"""
	if len(args.config) < 1:
		raise Exception("Please tell me the configs")

	configs = [get_config(c) for c in args.config]

	print("Generating PGO data")
	for c in configs:
		if c.use:
			config = copy(c)
			config.use = False
			config.gen = True
			sig = config.get_signature()
			print(f"\n\nRunning {sig}")
			run_game(args.game, config, debug=args.debug)

	print("Starting benchmark")
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

	# Write into file
	with open_data() as f:
		for config, res in results.items():
			sig = config.get_signature()
			times = [r.frame_time for r in res]
			f.write(f'bench["{args.game}-{sig}"] = {times}\n')

def analysis(args):
	"""Run the PGO analyzation pass, this needs existing PGO generated data"""
	if len(args.config) > 1:
		raise Exception("Analysis only uses one config")
	if len(args.config) == 1:
		config = get_config(args.config[0])
	else:
		config = RunConfig()

	gen_config = copy(config)
	gen_config.gen = True
	sig = gen_config.get_signature()
	print(f"\n\nRunning {sig}")
	run_game(args.game, gen_config, debug=args.debug)

	an_config = copy(config)
	an_config.use = True
	an_config.analysis = True
	sig = an_config.get_signature()
	analysis_file = "/tmp/mydriveranalysis.txt"
	if os.path.isfile(analysis_file):
		os.remove(analysis_file)

	print(f"\n\nAnalyzing {sig}")
	run_game(args.game, an_config, debug=args.debug)

	dead_code = []
	uniformity = []
	counters = []
	with open(analysis_file) as f:
		first = True
		for l in f:
			l = l.strip()

			if l.startswith("Compiling"):
				if not first:
					dead_code.append((zero, total))
					uniformity.append({
						"static": uni_static,
						"dynamic": uni_dynamic,
						"divergent": uni_divergent,
					})
					counters.append(ctrs)
				else:
					first = False

				zero = 0
				total = 0
				ctrs = []

				uni_static = {
					"Condition": 0,
					"Address": 0,
					"LoadValue": 0,
				}
				uni_dynamic = {
					"Condition": 0,
					"Address": 0,
					"LoadValue": 0,
				}
				uni_divergent = {
					"Condition": 0,
					"Address": 0,
					"LoadValue": 0,
				}
			elif l == "Count is 0":
				zero += 1
				total += 1
				ctrs.append(0)
			elif l.startswith("Count is "):
				total += 1
				ctrs.append(int(l[l.rfind(" ") + 1:]))
			elif l.endswith("Static uniform"):
				typ = l[:l.find(":")]
				uni_static[typ] += 1
			elif l.endswith("Dynamic uniform"):
				typ = l[:l.find(":")]
				uni_dynamic[typ] += 1
			elif l.endswith("Divergent"):
				typ = l[:l.find(":")]
				uni_divergent[typ] += 1
			elif len(l) != 0:
				raise Exception(f"Unknown line '{l}'")

		if not first:
			dead_code.append((zero, total))
			uniformity.append({
				"static": uni_static,
				"dynamic": uni_dynamic,
				"divergent": uni_divergent,
			})
			counters.append(ctrs)

	print(f"Uniformity: {uniformity}")
	print(f"Counters: {counters}")
	print(f"Dead code: {dead_code}")
	print(f"Aggregated uniformity: {aggregate(uniformity)}")

	# Write into file
	with open_data() as f:
		f.write(f'counters["{args.game}-{sig}"] = {counters}\n')
		f.write(f'uniformity["{args.game}-{sig}"] = {uniformity}\n')

def get_config(options):
	config = RunConfig()

	for o in options.split(","):
		if o == "":
			pass
		elif o == "gen":
			config.gen = True
		elif o == "use":
			config.use = True
		elif o == "late":
			config.late = True
		elif o == "per_wave":
			config.per_wave = True
		elif o == "uniform":
			config.uniform = True
		elif o == "remove":
			config.remove = True
		elif o == "non_atomic":
			config.non_atomic = True
		elif o == "analysis":
			config.analysis = True
		else:
			raise Exception(f"Unknown PGO option {o}")

	return config

def main():
	actions = {
		"run": run,
		"bench": bench,
		"analysis": analysis,
		"registers": registers,
	}

	parser = argparse.ArgumentParser(description="Benchmarks!")
	parser.add_argument("action", choices=list(actions.keys()) + ["setup", "teardown"])
	game_names = [g.name for g in games]
	parser.add_argument("-g", "--game", choices=game_names)
	parser.add_argument("-d", "--debug", action="store_true", help="Start in a debugger")
	parser.add_argument("-c", "--config", action="append", help="Enabled PGO options, comma-separated")

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
