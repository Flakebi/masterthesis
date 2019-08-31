import io
import os
from os import path
import shutil
import subprocess

from utils import *

# Warhammer 40,000: Dawn of War III
name = "dow3"

def run(env, remove_cache, debug, sig):
	args = ["/home/sebi/Masterarbeit/repo/scripts/dow3_start.sh"]

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

	needle = "Average fps"
	p = output.find(needle) + len(needle)
	fps = float(output[p:].strip())
	print(f"Got {fps} fps and {1/fps} s")
	return RunResult(1/fps)
