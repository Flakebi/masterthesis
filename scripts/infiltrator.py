import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess

from utils import *

name = "infiltrator"

def run(env, remove_cache, debug, sig):
	env["SDL_VIDEODRIVER"] = "x11"

	if debug:
		args = ["lldb", "Engine/Binaries/Linux/UE4Game", "--"]
	else:
		args = ["Engine/Binaries/Linux/UE4Game"]

	subprocess.run(args + ["../../../InfiltratorDemo/InfiltratorDemo.uproject"],
		check=True, env={**env, **dict(os.environ)}, cwd="/mnt/bigdata/Dateien/Programme/Games/InfiltratorDemo")
	time = 1
	return RunResult(time)
