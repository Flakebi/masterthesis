#!/usr/bin/env python3
import argparse
from os import path

from data import *
from utils import *

games = {"dota": "Dota 2", "ashes": "Ashes", "dow3": "Warhammer",
		"f12017": "F1 2017", "madmax": "Mad Max", "switch": "Switch vm",
		"infiltrator": "Unreal Infiltrator"}

def overhead(args):
	configs = ["", "gen-wave-late", "gen-wave-late-non_atomic"]
	legend = ["Normal", "Atomic, per unit", "Non-atomic, per unit"]
	if args.diagram:
		overhead_diag(args, configs, legend)
	else:
		overhead_tab(args, configs, legend)

def overhead_diag(args, configs, legend):
	for config in configs:
		print(f"\\addplot+[error bars/.cd,y dir=both,y explicit] coordinates {{")
		for game in sorted(games.keys()):
			key = f"{game}-{config}"
			if key in bench and game != "switch":
				val = Value.avg([i * 1000 for i in bench[key]])
				print(f"({game},{val.val}) +- (0,{val.error})")

		print("};")

	print(f"\\legend{{{{{'},{'.join(legend)}}}}}")

def overhead_tab(args, configs, legend):
	print(r"""\begin{tabular}{l|l|l|l}
\textbf{Game} & \textbf{Config} & \textbf{Time per frame} & \textbf{Overhead}\\ """)

	for game in sorted(games.keys()):
		first = True
		for config, leg in zip(configs, legend):
			key = f"{game}-{config}"
			if key in bench and game != "switch":
				avg_val = Value.avg(bench[key])

				if first:
					overhead = ""
					start = f"\\hline\n{games[game]}"
					base = avg_val
					first = False
				else:
					overhead = ((avg_val / base - 1) * 100).tex_str("\\percent")
					start = ""

				avg_str = (avg_val * 1000).tex_str("\\milli\\second")
				print(f"""{start} & {leg} & {avg_str} & {overhead}\\\\\
""")

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

def unused_code_summary(args):
	used_games = []
	for game in sorted(games.keys()):
		for k, v in counters.items():
			if not k.startswith(game):
				continue

			used_games.append((game, v))

	print(f"""
\\begin{{axis}}[
	ybar,
	enlarge x limits=0.1,
	symbolic x coords={{{",".join([g for g, _ in used_games])}}},
	xticklabels={{{",".join([games[g] for g, _ in used_games])}}},
	xtick=data,
	xticklabel style={{text width=2.5cm,align=center}},
	ylabel={{Unused blocks [\SI{{}}{{\percent}}]}},
	ymin=0,
	ymax=119,
	grid=both,
	nodes near coords,
	every node near coord/.append style={{rotate=90, anchor=west}},
	bar width=0.5cm,
	legend style={{at={{(1,1)}},anchor=north east}},
]

\\addplot[
	fill=tumblue,
] table[header=false, row sep=\\\\] {{\
""")

	for game, v in used_games:
		v2 = get_non_zero(v)

		all_bbs = 0
		zero_bbs = 0
		for pipeline in v2:
			all_bbs += len(pipeline)
			for c in pipeline:
				if c == 0:
					zero_bbs += 1

		print(f"{game}\t{zero_bbs / all_bbs * 100}\\\\")

	print("};\n\\end{axis}")

def performance(args):
	configs = ["", "use-wave-late", "use-wave-late-remove"]
	legend = ["Normal", "PGO", "PGO + removing blocks"]
	if args.diagram:
		performance_diag(args, configs, legend)
	else:
		performance_tab(args, configs, legend)

def performance_diag(args, configs, legend):
	for config in configs:
		print(f"\\addplot+[error bars/.cd,y dir=both,y explicit] coordinates {{")
		for game in sorted(games.keys()):
			key = f"{game}-{config}"
			if key in bench:
				val = Value.avg([i * 1000 for i in bench[key]])
				print(f"({game},{val.val}) +- (0,{val.error})")

		print("};")

	print(f"\\legend{{{{{'},{'.join(legend)}}}}}")

def performance_tab(args, configs, legend):
	print(r"""\begin{tabular}{l|l|l|l}
\textbf{Game} & \textbf{Config} & \textbf{Time per frame} & \textbf{Difference}\\ """)

	for game in sorted(games.keys()):
		first = True
		for config, leg in zip(configs, legend):
			key = f"{game}-{config}"
			if key in bench:
				avg_val = Value.avg(bench[key])

				if first:
					overhead = ""
					start = f"\\hline\n{games[game]}"
					base = avg_val
					first = False
				else:
					overhead = ((avg_val / base - 1) * 100).tex_str("\\percent")
					start = ""

				avg_str = (avg_val * 1000).tex_str("\\milli\\second")
				print(f"""{start} & {leg} & {avg_str} & {overhead}\\\\\
""")

	print(r"\end{tabular}")

def registers_fun(args):
	configs = ["", "use-wave-late", "use-wave-late-remove"]
	legend = ["Normal", "PGO", "PGO + removing blocks"]

	if not args.game:
		print("Need to get a type (cs/vs/ps) for registers")
		return

	typ, reg_typ = args.game.split("-")
	if typ == "cs":
		start_index = 0
	elif typ == "vs":
		start_index = 2
	elif typ == "ps":
		start_index = 4
	else:
		print(f"{typ} is a wrong type, try cs/vs/ps")
		return

	if reg_typ == "sgpr":
		start_index += 1
	elif reg_typ != "vgpr":
		print(f"{reg_typ} is a wrong type, try vgpr/sgpr")
		return

	for config in configs:
		print("\\addplot coordinates {")
		for game in sorted(games.keys()):
			key = f"{game}-{config}"
			if key in registers:
				regs = registers[key]
				count = 0
				amount = 0
				for v in regs.values():
					if v[start_index] != 0:
						count += v[start_index]
						amount += 1
				count /= amount

				print(f"({game},{count})")
		print("};")

	print(f"\\legend{{{{{'},{'.join(legend)}}}}}")

def uniform(args, key):
	configs = ["static", "dynamic", "divergent"]
	amount = {game: 0 for game in games}
	counters = {}
	for config in configs:
		for game in games.keys():
			counter = 0
			uni_key = f"{game}-use-wave-late-uniform"
			if uni_key not in uniformity:
				continue

			for shader in uniformity[uni_key]:
				counter += shader[config][key]

			if not config in counters:
				counters[config] = {}
			counters[config][game] = counter
			amount[game] += counter

	for config in configs:
		print("\\addplot coordinates {")
		for game in sorted(games.keys()):
			if game in counters[config]:
				count = counters[config][game] / amount[game] * 100
				print(f"({game},{count})")
		print("};")

def uniform_branches(args):
	uniform(args, "Condition")

def uniform_loads(args):
	uniform(args, "LoadValue")

def register_scatter(args):
	# Analyze vgprs only
	xconfig = "use-wave-late"
	yconfig = "use-wave-late-remove"
	indices = [0, 2, 4]
	games = ["dota", "madmax"]

	print(r"""
\addplot[scatter,only marks,scatter src=explicit symbolic]
coordinates {""")
	for game in games:
		xdata = registers[f"{game}-{xconfig}"]
		ydata = registers[f"{game}-{yconfig}"]
		for k in xdata.keys():
			if k not in ydata:
				continue

			# Count of shader types used in the pipeline
			for i in indices:
				if xdata[k][i] != 0:
					print(f"({xdata[k][i]},{ydata[k][i]}) [{game}]")

	print("};")

def get_occupancy(regs):
	max_regs = 256

	# Round registers up to a multiple of 4
	regs = (regs + 3) // 4 * 4
	return max_regs // regs

def register_occupancy(args):
	# Analyze vgprs only
	xconfig = "use-wave-late"
	yconfig = "use-wave-late-remove"
	indices = [0, 2, 4]
	games = ["dota", "madmax"]

	data_size = 10
	print(f"""
\\addplot [matrix plot*,point meta=explicit,mesh/cols={data_size},mesh/rows={data_size}]
table [meta index=2,header=false,row sep=\\\\] {{""")
	data = [[0 for _ in range(data_size)] for _ in range(data_size)]
	for game in games:
		xdata = registers[f"{game}-{xconfig}"]
		ydata = registers[f"{game}-{yconfig}"]
		for k in xdata.keys():
			if k not in ydata:
				continue

			# Count of shader types used in the pipeline
			for i in indices:
				if xdata[k][i] != 0:
					x = get_occupancy(xdata[k][i])
					y = get_occupancy(ydata[k][i])
					if y <= data_size and x <= data_size:
						data[y - 1][x - 1] += 1

	for y, row in enumerate(data):
		for x, val in enumerate(row):
			print(f"{x + 1}\t{y + 1}\t{val}\\\\")

	print("};")

def data(args):
	xconfig = "use-wave-late"
	indices = [0, 2, 4]

	for game in sorted(games.keys()):
		print(f"\n{game}")

		# Count shaders
		count = 0
		xdata = registers[f"{game}-{xconfig}"]
		for x in xdata.values():
			for i in indices:
				if x[i] != 0:
					count += 1
		print(f"{count} shaders")

def main():
	actions = {
		"overhead": overhead,
		"counter-dist1": lambda args: counter_dist(args, counter_dist1),
		"counter-dist2": lambda args: counter_dist(args, counter_dist2),
		"unused-code": unused_code,
		"bbs": bbs,
		"max-bbs": max_bbs,
		"unused-code-summary": unused_code_summary,
		"performance": performance,
		"registers": registers_fun,
		"uniform-branches": uniform_branches,
		"uniform-loads": uniform_loads,
		"register-scatter": register_scatter,
		"register-occupancy": register_occupancy,
		"data": data,
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
