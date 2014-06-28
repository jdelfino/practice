import sys
import time
import pprint
from collections import defaultdict

gen_cache = {}
find_cache = {}

times = defaultdict(float)

###### assorted helpers #######

''' memoize results in the given cache '''
def memoize(cache):
	def wrap(func):
		def wrapped(*args):
			if args in cache:
				return cache[args]
			rval = func(*args)
			cache[args] = rval
			return rval
		wrapped.__name__ = func.__name__
		return wrapped
	return wrap

''' time a function in the global times dictionary '''
def timeit(func, *args):
	tic = time.time()
	rval = func(*args)
	times[func.__name__] += time.time() - tic
	return rval

''' get the approximate size of a dictionary containing primitive types '''
def size_of_dict(d):
	return sum(sys.getsizeof(x) + sys.getsizeof(y) for x,y in d.iteritems())

''' Compare the gray code answers for a list of functions '''
def compare(n, c, *args):
	answers = {}
	for func in args:
		answers[func.__name__] = timeit(func, n,c)

	if len(set(answers.values())) != 1:
		assert False, "n=%s c=%s %s" % (n,c,pprint.pformat(answers))

####### Gray code generators #########

''' find just the c'th gray code of length n, rather than generating the entire sequence '''
def findgray(n,c):
	if n == 1:
		return str(c)

	if c >= 2**(n-1):
		return '1' + findgray(n - 1, 2**n - 1 - c)
	else:
		return '0' + findgray(n - 1, c)

''' findgray, written using iteration rather than recursion.
	used to evaluate cost of function call overhead '''
def iterative_findgray(n,c):
	orig_c = c
	rval = ''
	while(n > 1):
		if c >= 2**(n-1):
			rval += '1'
			c = 2**n - 1 - c
		else:
			rval += '0'
		n = n - 1

	return rval + str(c)

''' Calculate the c'th gray code with by brute force - 
	generate the entire sequence of n-length gray codes, and take the c'th value '''
def brutegray(n, c):
	return generate(n)[c]

''' Recursive helper to generate gray codes of length n '''
def generate(n):
	if n < 1:
		raise Exception("Invalid index %s" % n)

	if n == 1:
		return ['0', '1']

	base = generate(n-1)
	return ['0' + x for x in base] + ['1' + x for x in reversed(base)]

###### Memoize wrappers for performance comparison #######

@memoize(find_cache)
def cached_findgray(n,c):
	return findgray(n,c)

@memoize(gen_cache)
def cached_generate(n):
	return generate(n)

def cached_brutegray(n,c):
	return cached_generate(n)[c]

def main():
	if sys.argv[1] == 'test':
		global find_time
		global gen_time
		for n in range(1,20):
			print "Checking n=%s" % n
			for c in range(2**n):
				#compare(n, c, findgray, iterative_findgray, cached_findgray, brutegray, cached_brutegray)
				compare(n, c, iterative_findgray, cached_brutegray)

		print
		print "Times:"
		for name, val in sorted(times.items(), key=lambda x:x[1]):
			print "%.3f: %s" % (val, name)

		print
		print "Approx. memory usage:"
		print "Generate cache: %.0f kb" % (size_of_dict(gen_cache) / 1024)
		print "Find cache: %.0f kb" % (size_of_dict(find_cache) / 1024)

	else:
		n = int(sys.argv[1])
		c = int(sys.argv[2])
		findgray(n, c)


if __name__ == '__main__':
	main()