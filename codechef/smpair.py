import fileinput
import itertools
''' http://www.codechef.com/LTIME13/problems/SMPAIR '''

def main():
	fi = fileinput.input()
	ncases = int(fi.readline())

	for n in range(ncases):
		nints = int(fi.readline())
		nums = fi.readline().strip().split()
		nums = sorted(int(x) for x in nums)
		print nums[0] + nums[1]

if __name__ == '__main__':
	main()