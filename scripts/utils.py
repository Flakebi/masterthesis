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

class Value:
	def __init__(self, val, error):
		self.val = val
		self.error = error

	def __add__(self, other):
		"""Propagate errors via quadratic addition"""
		if isinstance(other, Value):
			return Value(self.val + other.val, sqrt(self.error**2 + other.error**2))
		else:
			return Value(self.val + other, self.error)

	def __sub__(self, other):
		if isinstance(other, Value):
			return Value(self.val - other.val, sqrt(self.error**2 + other.error**2))
		else:
			return Value(self.val - other, self.error)

	def __mul__(self, other):
		if isinstance(other, Value):
			return Value(self.val * other.val, sqrt((self.error * other.val)**2
				+ (other.error * self.val)**2))
		else:
			return Value(self.val * other, self.error * other)

	def __truediv__(self, other):
		if isinstance(other, Value):
			return Value(self.val / other.val, sqrt((self.error / other.val)**2
				+ (other.error * self.val / other.val**2)**2))
		else:
			return Value(self.val / other, self.error / other)

	def get_val_error(self):
		error = 1
		while error > self.error:
			error /= 10
		while error <= self.error:
			error *= 10

		# error is      0.00100
		# self.error is 0.000xx

		# 2 digits for the error if it starts with 1 or 2, 1 digit otherwise
		digits = 1

		# Check if we need to round up
		if self.error > error - error / 10:
			digits = 2
			# error is correct
		else:
			error /= 10
			# We have two digits up to <= 0.00029
			if self.error <= 2.9 * error:
				digits = 2

		# print(f"{error}, {digits}")

		val_digits = 0
		if digits == 2:
			error /= 10

		if error >= 10 and digits == 2:
			digits = 0
		elif error >= 1:
			digits -= 1

		i = error
		while i < 1:
			i *= 10
			val_digits += 1

		# print(f"{digits}, {val_digits}")

		# Ceil error and rount value
		value = round(self.val / error) * error
		error = ceil(self.error / error) * error

		val = "{0:.{1}f}".format(value, val_digits)
		error = "{0:.{1}f}".format(error, val_digits)
		return val, error

	def __str__(self):
		val, error = self.get_val_error()
		return f"{val} ± {error}"

	def tex_str(self, unit):
		val, error = self.get_val_error()
		return f"\\SI{{{val} \pm {error}}}{{{unit}}}"

	def avg(vals):
		return Value(avg(vals), deviationStudentT(vals))

	def test_error():
		assert str(Value(1, 1)) == "1.0 ± 1.0"
		assert str(Value(1, 0.1)) == "1.00 ± 0.10"
		assert str(Value(1, 0.2)) == "1.00 ± 0.20"
		assert str(Value(1, 0.29)) == "1.00 ± 0.29"
		assert str(Value(1, 0.291)) == "1.0 ± 0.3"
		assert str(Value(0.124, 0.0291)) == "0.12 ± 0.03"
		assert str(Value(0.1251, 0.0291)) == "0.13 ± 0.03"

		assert str(Value(2, 3)) == "2 ± 3"
		assert str(Value(20, 3)) == "20 ± 3"
		assert str(Value(20, 9.1)) == "20 ± 10"

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
