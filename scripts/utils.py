from math import *

class RunConfig:
	def __init__(self, gen=False, use=False, per_wave=False, late=False, uniform=False):
		self.gen = gen
		self.use = use
		self.per_wave = per_wave
		self.late = late
		self.uniform = uniform

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
	parts= haystack.split(needle, n + 1)
	if len(parts) <= n + 1:
		return -1
	return len(haystack) - len(parts[-1]) - len(needle)
