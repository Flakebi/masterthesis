import io
import os
from os import path
import random
import shutil
import subprocess

from utils import *

name = "f12017"

def run(env, remove_cache, debug, sig):
	if debug:
		args = ["lldb", "/home/sebi/Masterarbeit/repo/scripts/f12017_start.sh", "--"]
	else:
		args = ["/home/sebi/Masterarbeit/repo/scripts/f12017_start.sh"]

	# if remove_cache:
	env["AMDVLK_VERSION_XOR"] = str(random.randint(0, 65535))

	with open("/tmp/steamgameenv", "w") as f:
		for k, v in env.items():
			f.write(f"export {k}='{v}'\n")

	subprocess.run(args, check=True, env={**env, **dict(os.environ)})
	with subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True,
		env=env) as p, io.StringIO() as buf:

		for line in p.stdout:
			print(line, end='')
			buf.write(line)
		output = buf.getvalue()

	needle = "Average frame time"
	p = output.find(needle) + len(needle)
	time = float(output[p:].strip()) / 1000
	print(f"Got {1/time} fps and {time} s")
	return RunResult(time)
