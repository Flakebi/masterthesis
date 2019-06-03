#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
	print("Usage: ./ashes_extract.py <Output.txt>")
	sys.exit(1)

res = []
with open(sys.argv[1], encoding = 'latin1') as f:
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

print(res)
