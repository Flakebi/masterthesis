from math import *

class RunConfig:
	def __init__(self, gen=False, use=False, per_wave=False, late=False, uniform=False, analysis=False, remove=False):
		self.gen = gen
		self.use = use
		self.per_wave = per_wave
		self.late = late
		self.uniform = uniform
		self.analysis = analysis
		self.remove = remove

	def get_signature(self):
		sig = ""
		if self.gen:
			if len(sig) != 0:
				sig += "-"
			sig += "gen"
		if self.use:
			if len(sig) != 0:
				sig += "-"
			sig += "use"
		if self.per_wave:
			if len(sig) != 0:
				sig += "-"
			sig += "wave"
		if self.late:
			if len(sig) != 0:
				sig += "-"
			sig += "late"
		if self.uniform:
			if len(sig) != 0:
				sig += "-"
			sig += "uniform"
		if self.remove:
			if len(sig) != 0:
				sig += "-"
			sig += "remove"
		return sig

class RunResult:
	def __init__(self, frame_time):
		self.frame_time = frame_time

def avg(xs):
	return sum(xs) / len(xs)

def deviation(xs):
	"""How much do measurements variate?"""
	a = avg(xs)
	return sqrt(sum([(x - a) ** 2 for x in xs]) / (len(xs) - 1))

def deviationAvg(xs):
	"""In which interval is the average probably?
	This does decrease with more measurements."""
	return deviation(xs) / sqrt(len(xs))

def deviationStudentT(xs):
	# Vertrauensniveau: 68.3%
	#t_n = [0] * 2 + [1.3, 0.76, 0.6, 0.51, 0.45, 0.40, 0.38, 0.36, 0.34] + [0.27] * 9 + [0.23] * 10 + [0.19] * 20 + [0.14] * 50 + [0.1] * 100
	#return t_n[len(xs)] * deviation(xs)
	t = [0] * 2 + [1.84, 1.32, 1.20, 1.15, 1.11, 1.10, 1.08, 1.07] + [1.06] * 10 + [1.03] * 10 + [1.02] * 20 + [1.01] * 50
	return t[len(xs)] * deviationAvg(xs)

# Under CC-BY-SA from https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
def findnth(haystack, needle, n):
	parts = haystack.split(needle, n + 1)
	if len(parts) <= n + 1:
		return -1
	return len(haystack) - len(parts[-1]) - len(needle)

def to10slots(data):
	"""Sum data into 10 slots"""
	res = [0] * 10
	for i, d in enumerate(data):
		res[i * 10 // len(data)] += d
	return res

def to_slots5(data):
	"""Sum data into slots where each slot sums up 5 numbers"""
	res = [0] * ((len(data) + 4) // 5)
	for i, d in enumerate(data):
		res[i // 5] += d
	return res

def get_slotted_data(data, maximum):
	"""Match x coordinates to data in slots"""
	step = maximum / len(data)
	return [(int((i + 1) * step), d) for i, d in enumerate(data)]

def create_histograms(data):
	# Filter out unused shaders
	prev_len = len(data)
	data = [(z, c) for z, c in data if z != c]
	print(f"{100 - len(data) / prev_len * 100}% of shaders is unused")
	max_bbs = max([c for _, c in data])
	print(f"Up to {max_bbs} basic blocks")

	dead_code = [(0, 0)] * (max_bbs + 1)
	for z, c in data:
		a, b = dead_code[c]
		dead_code[c] = (a + z, b + c)

	def safe_divide(z, c):
		if c == 0:
			return 0
		else:
			return z / c

	dead_code = [safe_divide(z, c) for z, c in dead_code]
	print(f"Dead code: {to_slots5(dead_code)}")

	bb_count = [0] * (max_bbs + 1)
	for _, c in data:
		bb_count[c] += 1

	print(f"BB count: {to_slots5(bb_count)}")

	print("\nDead code")
	for a, b in get_slotted_data(to_slots5(dead_code), max_bbs):
		print(f"{a}\t{b}")
	for i, a in enumerate(to_slots5(dead_code)):
		print(f"{i*5+2.5}\t{a}")

	print("\nBB count")
	for i, a in enumerate(to_slots5(bb_count)):
		print(f"{i*5+2.5}\t{a}")

	# for a, b in get_slotted_data(to_slots5(bb_count), max_bbs):
		# print(f"{a}\t{b}")

def aggregate(vals):
	res = {}
	for val in vals:
		for k, l in val.items():
			if k not in res:
				res[k] = {}
			for k2, v in l.items():
				if k2 not in res[k]:
					res[k][k2] = v
				else:
					res[k][k2] += v

	return res
