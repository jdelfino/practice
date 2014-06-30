import fileinput
import itertools
from fractions import gcd
import sys
import random

def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True

def smart(nums):
	num = len(nums)

	count = 0
	for xnum, x in enumerate(itertools.islice(nums, num-2)):

		for ynum, y in enumerate(itertools.islice(nums, xnum+1, num - 1), xnum+1):
			outer_gcd = gcd(xnum, ynum)
			if outer_gcd == 1:
			 	count += num - ynum - 1
				continue
			else:
				for znum, z in enumerate(itertools.islice(nums, ynum+1, None), ynum+1):
					if gcd(z, outer_gcd) == 1:
						count += 1

	return count

def dumb(nums):
	mod_nums = [(x,y) for x,y in enumerate(nums)]
	res = [(x[0],y[0],z[0]) for x,y,z in itertools.combinations(mod_nums, 3) if gcd(x[1],gcd(y[1],z[1])) == 1]
	return len(res)

def compare(nums):
	sm = smart(nums)
	du = dumb(nums)

	if sm != du:
		print ' '.join(str(x) for x in nums)

def main():
	if len(sys.argv) > 1:
		if sys.argv[1] == 'test':
			for j in range(3, int(sys.argv[3])):
				print j
				for i in range(int(sys.argv[2])):
					nums = [random.randint(1,10**6) for x in range(j)]
					compare(nums)
			return

		print sys.argv[1]
		print ' '.join(str(random.randint(1,10**6)) for x in range(int(sys.argv[1])))
		return

	fi = fileinput.input()

	num = int(fi.readline().strip())
	nums = [int(x) for x in fi.readline().strip().split(" ")]

	print smart(nums)
	#compare(nums)

if __name__ == '__main__':
	main()