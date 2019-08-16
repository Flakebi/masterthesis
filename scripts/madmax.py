import io
import os
from os import path
import shutil
import subprocess

from utils import *

name = "madmax"

def run(env, remove_cache, debug, sig):
	args = ["/home/sebi/Masterarbeit/repo/scripts/madmax_start.sh"]

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
