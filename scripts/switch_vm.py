import io
import os
from os import path
import shutil
import subprocess

from utils import *

name = "switch"

def run(env, remove_cache, debug, sig):
	if debug:
		args = ["lldb", "../../../target/debug/triangle", "--"]
	else:
		args = ["../../../target/debug/triangle"]
	with subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True,
		env=env, cwd="/home/sebi/Dokumente/Dateien/Programme/Libraries/vulkano/examples/src/bin") as p, io.StringIO() as buf:

		for line in p.stdout:
			print(line, end='')
			buf.write(line)
		output = buf.getvalue()

	p = output.find("Total:") + 6
	p2 = output.find("f", p)
	fps = float(output[p:p2].strip())
	print(f"Got {fps} fps and {1/fps} s")
	return RunResult(1 / fps)
