from fractions import gcd

'''http://apps.topcoder.com/wiki/display/tc/SRM+616'''

def lcm(*args):
	if not args:
		raise Exception
	if len(args) < 2:
		return args[0]
	if len(args) >= 2:
		return lcm((args[0] * args[1]) / gcd(args[0], args[1]), *args[2:])

class WakingUp:
	def maxSleepiness(self, period, start, volume, D):
		full_period = lcm(*period)
		#print full_period

		min_S = 0
		S = 0
		for tic in range(1, full_period):
			S += D
			for p,s,v in zip(period, start, volume):
				#print tic, s, (tic -s), (tic -s) % p
				if (tic >= s) and ((tic - s) % p == 0):
					#print "alarm %s at %s" % (v, tic)
					S -= v
			min_S = min(S, min_S)
			#print "tic: %s, S: %s, min_S: %s" % (tic, S, min_S)

		#print "checking full", S, min_S
		full_start = S
		for tic in range(full_period, full_period*2):
			S += D
			for p,s,v in zip(period, start, volume):
				if (tic - s) % p == 0:
					#print "alarm %s at %s" % (v, tic)					
					S -= v
			min_S = min(S, min_S)
			#print "tic: %s, S: %s, min_S: %s" % (tic, S, min_S)

		if S < full_start:
			#print "sleepiness decreases forever", S, full_start
			# S will decrease forever
			return -1

		#print min_S
		return -1*min_S

def tests():
	yield ([2,3], [1,2], [3,4], 3, 2)
	yield ([1], [1], [17], 17, 0)
	yield ([1], [1], [23], 17, -1)
	yield ([9,2,5,5,7], [6,1,4,1,6], [71,66,7,34,6], 50, 78)
	yield ([5,6,5,3,8,3,4], [1,1,3,2,6,3,3], [42,85,10,86,21,78,38], 88, -1)

def main():

	inst = WakingUp()
	for num, (period, start, volume, D, answer) in enumerate(tests()):
		res = inst.maxSleepiness(period, start, volume, D)
		if res != answer:
			print "%s WRONG, expected: %2d, got: %2d, p: %s, s: %s, v: %s, D: %s" % (num, answer, res if res != None else -2, period, start, volume, D)
		else:
			print "%s CORRECT" % num


if __name__ == '__main__':
	main()