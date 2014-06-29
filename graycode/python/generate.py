import sys
import time
import pprint
from collections import defaultdict

''' Generate gray codes by various methods, and compare their speed 
For an explanation of gray codes see: https://en.wikipedia.org/wiki/Gray_code 

There's also a good bit of gratuitous inspection used to support passing method names_to_funcs
in from the command line. Overkill for something of this size, but good practice'''

gen_cache = {}
find_cache = {}
gray_methods = []

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
		wrapped.__doc__ = func.__doc__
		return wrapped
	return wrap

def public(func):
	def wrapped(*args, **kwargs):
		return func(*args, **kwargs)
	wrapped.__name__ = func.__name__
	wrapped.__doc__ = func.__doc__
	gray_methods.append(wrapped)
	return wrapped


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
	return answers.values()[0]

def names_to_funcs(funcnames):
	if 'all' in funcnames: 
		return gray_methods
	else:
		return [globals()[x] for x in funcnames] 

	return globals()[funcname] #bleh

''' Recursive helper to generate gray codes of length n '''
def generate(n):
	if n < 1:
		raise Exception("Invalid index %s" % n)

	if n == 1:
		return ['0', '1']

	base = generate(n-1)
	return ['0' + x for x in base] + ['1' + x for x in reversed(base)]

@memoize(gen_cache)
def cached_generate(n):
	return generate(n)

####### Gray code generators #########

@public
def findgray(n,c):
	''' find just the c'th gray code of length n, rather than generating the entire sequence '''
	if n <= 1:
		return str(c)

	if c >= 2**(n-1):
		return '1' + findgray(n - 1, 2**n - 1 - c)
	else:
		return '0' + findgray(n - 1, c)

@public
def iterative_findgray(n,c):
	''' findgray, written using iteration rather than recursion.
	used to evaluate cost of function call overhead '''
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

@public
def brutegray(n, c):
	''' Calculate the c'th gray code with by brute force - 
	generate the entire sequence of n-length gray codes, and take the c'th value '''
	return generate(n)[c]

@public
@memoize(find_cache)
def cached_findgray(n,c):
	''' recursive findgray with memoization '''
	return findgray(n,c)

@public
def cached_brutegray(n,c):
	''' brutegray with memoization '''
	return cached_generate(n)[c]

def usage():
	print "Usage: "
	print "python %s test <max length> [method name [,method name...]] to compare performance of methods on codes up to length n. " % (__file__)
	print "   default methods: iterative_findgray, cached_brutegray" 
	print "python %s <length> <index> [method name] to generate a single gray number." % (__file__)
	print "   default method: iterative_findgray"
	print 
	print "Available methods are: "
	for meth in gray_methods:
		print "%s: %s" % (meth.__name__, meth.__doc__)
	print "all: use all methods"

def main():
	if len(sys.argv) < 3:
		usage()
		return

	try:
		funcs = names_to_funcs(sys.argv[3:]) or [iterative_findgray, cached_brutegray]
	except KeyError, e:
		print "Function name %s not valid" % e
		print
		usage()
		return

	if sys.argv[1] == 'test':
		for n in range(1,int(sys.argv[2])):
			print "Checking n=%s" % n
			for c in range(2**n):
				compare(n, c, *funcs)

	else:
		try:
			n = int(sys.argv[1])
			c = int(sys.argv[2])
		except ValueError:
			usage()
			return
		print "%s-bit gray code #%s: %s" % (n,c, compare(n, c, *funcs))

	print
	print "Times:"
	for name, val in sorted(times.items(), key=lambda x:x[1]):
		print "%.3f: %s" % (val, name)

	print
	print "Approx. memory usage:"
	print "Generate cache: %.0f kb" % (size_of_dict(gen_cache) / 1024)
	print "Find cache: %.0f kb" % (size_of_dict(find_cache) / 1024)


if __name__ == '__main__':
	main()