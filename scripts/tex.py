#!/usr/bin/env python3
import argparse
from os import path

from data import *
from utils import *

games = {"dota": "Dota 2", "ashes": "Ashes", "dow3": "Dawn of War III", "f12017": "F1 2017", "madmax": "Mad Max"}

def overhead(args):
	# files = {"none": "No counters", "non-atomic-wave-late": "Non-atomic, per unit",
		# "late": "Atomic, per lane", "wave-late": "Atomic, per unit"}
	# file_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), "thesis", "data")
	data = [("No counters", overhead_normal),
		("Non-atomic, per unit", overhead_non_atomic_wave_late),
		("Atomic, per lane", overhead_late),
		("Atomic, per unit", overhead_wave_late),
	]

	dia = args.diagram
	if dia:
		pass
	else:
		print(r"""\begin{tabular}{l|l|l|l}
\textbf{Game} & \textbf{Config} & \textbf{Time per frame} & \textbf{Overhead}\\ """)

	# Sort by game not by column

	for g, name in games.items():
		first = True
		for col, d in data:
			for game, vals in d.items():
				if game != g:
					continue

				avg_val = Value.avg(vals)

				if dia:
					pass
				else:
					if first:
						overhead = ""
						start = f"\\hline\n{name}"
						base = avg_val
						first = False
					else:
						overhead = ((avg_val / base - 1) * 100).tex_str("\\percent")
						start = ""

					avg_str = (avg_val * 1000).tex_str("\\milli\\second")

					print(f"""{start} & {col} & {avg_str} & {overhead}\\\\\
""")

	if dia:
		pass
	else:
		print(r"\end{tabular}")

def counter_dist1(ctrs):
	bin_size = int(11222915000*2.5)
	bins = (max(ctrs) + bin_size - 1) // bin_size
	bins = 40
	bin_size = max(ctrs) // (bins - 1)

	bin_vals = [0] * bins
	for c in ctrs:
		if c != 0:
			bin_vals[c // bin_size] += 1

	return bin_size, bin_vals

def counter_dist2(ctrs):
	bin_size = int(11222/3.6)
	bins = (int(10e4) + bin_size - 1) // bin_size

	bin_vals = [0] * bins
	for c in ctrs:
		if c != 0:
			i = c // bin_size
			if i < len(bin_vals):
				bin_vals[i] += 1

	return bin_size, bin_vals

def counter_dist(args, f):
	if not args.game:
		print("Need to get a game for counter distribution")
		return

	for k, v in counters.items():
		if not k.startswith(args.game):
			continue

		ctrs = [item for l in v for item in l]

		print(f"""
\\addplot[
	fill=tumblue,
] table[header=false, row sep=\\\\] {{\
""")

		bin_size, bin_vals = f(ctrs)

		for i, b in enumerate(bin_vals):
			print(f"{i*bin_size + bin_size//2}\t{b}\\\\")

		print("} \closedcycle;")

def get_non_zero(v):
	v2 = []
	for pipeline in v:
		zeroes = 0
		for c in pipeline:
			if c == 0:
				zeroes += 1

		if zeroes != len(pipeline):
			v2.append(pipeline)
	return v2

def unused_code(args):
	if not args.game:
		print("Need to get a game for unused code")
		return

	for k, v in counters.items():
		if not k.startswith(args.game):
			continue

		print(f"""
\\addplot[
	fill=tumblue,
] table[header=false, row sep=\\\\] {{\
""")

		v2 = get_non_zero(v)

		#bins = 8
		#bin_size = max([len(l) for l in v]) // bins + 1
		bins = max([len(l) for l in v2]) + 1
		bin_size = 1
		bin_zero = [0] * bins
		bin_bbs = [0] * bins

		for pipeline in v2:
			i = len(pipeline) // bin_size
			zeroes = 0
			for c in pipeline:
				if c == 0:
					zeroes += 1

			bin_zero[i] += zeroes
			bin_bbs[i] += len(pipeline)

		for i in range(bins):
			print(f"{i*bin_size + bin_size//2}\t{safe_divide(bin_zero[i], bin_bbs[i]) * 100}\\\\")

		print("} \closedcycle;")

def bbs(args):
	if not args.game:
		print("Need to get a game for unused code")
		return

	for k, v in counters.items():
		if not k.startswith(args.game):
			continue

		print(f"""
\\addplot[
	smooth,
	fill=gray,
	fill opacity=0.4,
	draw=none,
] table[header=false, row sep=\\\\] {{\
""")

		v2 = get_non_zero(v)

		bins = 50
		bin_size = max([len(l) for l in v2]) // bins + 1

		bin_vals = [0] * bins

		for pipeline in v2:
			i = len(pipeline) // bin_size
			bin_vals[i] += 1

		for i in range(bins - 1, -1, -1):
			if bin_vals[i] != 0:
				break
			bin_vals.pop()

		for i in range(len(bin_vals)):
			print(f"{i*bin_size + bin_size//2}\t{bin_vals[i] / len(v2) / bin_size * 100}\\\\")

		print("} \closedcycle;")

def max_bbs(args):
	if not args.game:
		print("Need to get a game for max bbs")
		return

	for k, v in counters.items():
		if not k.startswith(args.game):
			continue

		v2 = get_non_zero(v)
		bins = max([len(l) for l in v2]) + 1
		print(f"{bins}")

def main():
	actions = {
		"overhead": overhead,
		"counter-dist1": lambda args: counter_dist(args, counter_dist1),
		"counter-dist2": lambda args: counter_dist(args, counter_dist2),
		"unused-code": unused_code,
		"bbs": bbs,
		"max-bbs": max_bbs,
	}

	parser = argparse.ArgumentParser(description="Generate tex code")
	parser.add_argument("action", choices=list(actions.keys()))
	parser.add_argument("-d", "--diagram", action="store_true", help="Emit diagram instead of table")
	parser.add_argument("-g", "--game")

	args = parser.parse_args()

	if args.action in actions:
		actions[args.action](args)

if __name__ == "__main__":
	main()
