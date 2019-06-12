#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess

import ashes
import dota
import vulkan_sponza

def get_signature(gen, use, per_wave, late, uniform):
	sig = ""
	if gen:
		if len(sig) != 0:
			sig += "-"
		sig += "gen"
	if use:
		if len(sig) != 0:
			sig += "-"
		sig += "use"
	if per_wave:
		if len(sig) != 0:
			sig += "-"
		sig += "wave"
	if late:
		if len(sig) != 0:
			sig += "-"
		sig += "late"
	if uniform:
		if len(sig) != 0:
			sig += "-"
		sig += "uniform"
	return sig

def run_game(name, remove_cache=True, debug=False, gen=False, use=False, per_wave=False, late=False, uniform=False):
	if (not gen and not use) and (per_wave or late or uniform):
		print("WARNING PGO options have no meaning when PGO is not in use")

	sig = get_signature(gen, use, per_wave, late, uniform)
	env = dict(os.environ)
	env["VK_ICD_FILENAMES"] = "/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json"
	pgo_sig = get_signature(False, False, per_wave, late, uniform)
	pgo_folder = f"/home/sebi/Downloads/pgo/{name}-{pgo_sig}"
	if gen:
		# Remove pgo folder and recreate
		shutil.rmtree(pgo_folder, ignore_errors=True)
		#os.makedirs(pgo_folder, exist_ok=True)
		os.makedirs(pgo_folder)
		env["AMDVLK_PROFILE_INSTR_GEN"] = f"{pgo_folder}/Pipeline_%i_%m.profraw"
	if use:
		env["AMDVLK_PROFILE_INSTR_USE"] = f"{pgo_folder}/Pipeline_%i.profdata"
	if per_wave:
		env["AMDVLK_PROFILE_PER_WAVE"] = "1"
	if late:
		env["AMDVLK_PROFILE_LATE"] = "1"
	if uniform:
		env["AMDVLK_PROFILE_UNIFORM"] = "1"

	if name == "dota":
		dota.run(env, remove_cache, debug, sig)
	elif name == "ashes":
		ashes.run(env, remove_cache, debug, sig)
	elif name == "sponza":
		vulkan_sponza.run(env, remove_cache, debug, sig)
	elif name == "test":
		subprocess.run("env", check=True, env=env, shell=True)
	else:
		raise Exception(f"Unknown game '{name}'")

	if gen:
		# Convert pgo data
		subprocess.run("/home/sebi/Masterarbeit/repo/scripts/convert_pipelines.sh", check=True, env=env, cwd=pgo_folder)

def setup():
	# echo profile_standard > /sys/class/drm/card0/device/power_dpm_force_performance_level
	# for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; echo performance > $f; end
	# echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo
	# Turn fan up, 255 is 100%
	# echo 1 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_enable
	# echo 150 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1
	pass

def teardown():
	# echo auto > /sys/class/drm/card0/device/power_dpm_force_performance_level
	# for f in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; echo powersave > $f; end
	# echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo
	# Fan to auto
	# echo 2 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1_enable
	pass

def diff(args):
	"""Run a game with different PGO options to compare the compiled output"""
	setup()
	try:
		# TODO
		while False:
			sig = get_signature(False, False, False, False, False)
			print(f"\n\nRunning {sig}")
			run_game(args.game, debug=args.debug, use=False)

			# Save pipelines
			orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
			pipe_folder = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
			shutil.rmtree(pipe_folder, ignore_errors=True)
			os.rename(orig_pipe_folder, pipe_folder)

		for gen in [True, False]:
			# This takes forever…
			#for per_wave in [True, False]:
			for per_wave in [True]:
				for late in [True, False]:
					sig = get_signature(gen, not gen, per_wave, late, False)
					print(f"\n\nRunning {sig}")
					run_game(args.game, debug=args.debug, gen=gen, use=not gen, per_wave=per_wave, late=late)

					# Save pipelines
					orig_pipe_folder = f"/home/sebi/Downloads/Pipelines/spvPipeline"
					pipe_folder = f"/home/sebi/Downloads/Pipelines/{args.game}-{sig}"
					shutil.rmtree(pipe_folder, ignore_errors=True)
					os.rename(orig_pipe_folder, pipe_folder)
	finally:
		teardown()

def main():
	parser = argparse.ArgumentParser(description="Benchmarks!")
	parser.add_argument("action", choices=["diff"])
	parser.add_argument("game", choices=["dota", "ashes", "sponza", "test"])
	parser.add_argument("-d", "--debug", help="Start in a debugger")

	args = parser.parse_args()

	if args.action == "diff":
		diff(args)

if __name__ == "__main__":
	main()
