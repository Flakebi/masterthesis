import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess

from utils import *

name = "ashes"

def run(env, remove_cache, debug, sig):
	subprocess.run(["/home/sebi/Masterarbeit/repo/scripts/ashes_start.sh"],
		check=True, env={**dict(os.environ), **env})

	# Find fps
	path = "/mnt/bigdata/Dateien/Programme/Steam/steamapps/compatdata/507490/pfx/drive_c/users/steamuser/My Documents/My Games/Ashes of the Singularity - Escalation"
	files = [f for f in listdir(path) if isfile(join(path, f)) and f.startswith("Output")]
	files.sort()
	file = files[-1]
	print(f"Searching fps in {file}")
	with open(join(path, file), "rb") as f:
		for l in f:
			if l.startswith(b"Total Time"):
				pos0 = l.find(b":") + 1
				pos1 = l.find(b"m", pos0)
				time = float(l[pos0:pos1].strip()) / 1000
				print(f"Got {1/time} fps and {time} s")
				return RunResult(time)
