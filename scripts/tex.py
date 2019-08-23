#!/usr/bin/env python3
import argparse
from os import path

from data import *
from utils import *

def overhead(args):
	# files = {"none": "No counters", "non-atomic-wave-late": "Non-atomic, per unit",
		# "late": "Atomic, per lane", "wave-late": "Atomic, per unit"}
	# file_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), "thesis", "data")
	games = {"dota": "Dota 2", "ashes": "Ashes"}
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
\textbf{Game} & \textbf{Config} & \textbf{Time per frame} & \textbf{Overhead}\\""")

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

					print(f"""{start} & {col} & {avg_str} & {overhead}\\\\""")

	if dia:
		pass
	else:
		print(r"\end{tabular}")

def main():
	actions = {
		"overhead": overhead,
	}

	parser = argparse.ArgumentParser(description="Generate tex code")
	parser.add_argument("action", choices=list(actions.keys()))
	parser.add_argument("-d", "--diagram", action="store_true", help="Emit diagram instead of table")

	args = parser.parse_args()

	if args.action in actions:
		actions[args.action](args)

if __name__ == "__main__":
	main()
