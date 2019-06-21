import os
from os import path
import shutil
import subprocess

from utils import *

name = "dota"

def run(env, remove_cache, debug, sig):
	cache_path = "/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota/shadercache"
	sig_cache_path = f"{cache_path}-{sig}"
	# Delete current cache
	shutil.rmtree(cache_path, ignore_errors=True)

	if not remove_cache:
		if path.isdir(sig_cache_path):
			# Restore cache
			os.rename(sig_cache_path, cache_path)
	else:
		shutil.rmtree(sig_cache_path, ignore_errors=True)

	# env VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json LD_LIBRARY_PATH=/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/bin/linuxsteamrt64 trace-cmd record -F -e amdgpu:amdgpu_vm_flush -e amdgpu:amdgpu_cs_ioctl -e amdgpu:amdgpu_sched_run_job -e '*fence:*fence_signaled' -e drm:drm_vblank_event -e drm:drm_vblank_event_queued /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/bin/linuxsteamrt64/dota2 +demo_quitafterplayback 1 +cl_showfps 2 +fps_max 0 -nosound -noassert +timedemoquit dota2-pts-1971360796 +timedemo_start 50000 +timedemo_end 51000 -novconsole
	env["SDL_VIDEODRIVER"] = "x11"
	env["LD_LIBRARY_PATH"] = "/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/bin/linuxsteamrt64"

	if debug:
		args = ["lldb", "/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/bin/linuxsteamrt64/dota2", "--"]
	else:
		args = ["/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/bin/linuxsteamrt64/dota2"]
	subprocess.run(args + [
		#"-sdl_displayindex", "1",
		"+demo_quitafterplayback", "1",
		"+cl_showfps", "2",
		"+fps_max", "0",
		"-nosound",
		"-noassert",
		"-novconsole",
		"+timedemoquit", "dota2-pts-1971360796",
		"+timedemo_start", "50000",
		"+timedemo_end", "51000",
	], check=True, env=env)

	# Backup cache
	os.rename(cache_path, sig_cache_path)

	with open("/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota/Source2Bench.csv", "r") as f:
		# Get last line
		for last in f:
			pass

	p = findnth(last, ",", 1)
	p2 = last.find(",", p + 1)
	fps = float(last[p + 1:p2].strip())
	print(f"Got {fps} fps and {1/fps} ms")
	return RunResult(1 / fps)
