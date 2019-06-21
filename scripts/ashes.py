import sys
from os import listdir
from os.path import isfile, join
import subprocess

from utils import *

name = "ashes"

def extract_file(name):
	res = []
	with open(name, encoding = 'latin1') as f:
		curName = ""
		for l in f:
			if l.startswith("== "):
				i = l.find("=", 3)
				if i != -1:
					curName = l[3:i].strip()
			elif l.startswith("Avg Framerate"):
				i = l.find(":")
				j = l.find("F", i)
				if i != -1 and j != -1:
					s = l[i+1:j].strip()
					try:
						fps = float(s)
						res.append((curName, fps))
					except:
						print(f"Failed to convert {s} to float")
	return res

def old_main():
	if len(sys.argv) == 2:
		print(extract_file(sys.argv[1]))
	elif len(sys.argv) == 4:
		path = sys.argv[1]
		files = [f for f in listdir(path) if isfile(join(path, f)) and f.startswith("Output")]
		files.sort()
		# TODO
	else:
		print("Usage: ./ashes_extract.py <Output.txt>")
		print("or     ./ashes_extract.py <starttime> <endtime>")
		print("e.g.   ./ashes_extract.py <path> 19_06_04_1518 19_06_04_1623")
		sys.exit(1)

def run(env, remove_cache, debug, sig):
	subprocess.run(["/home/sebi/Masterarbeit/repo/scripts/ashes_start.sh"],
		check=True, env=env)
	# Find fps
