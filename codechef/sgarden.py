import fileinput
from fractions import gcd

def lcm(nums):
	lcm = nums[0]
	for arg in nums[1:]:
		lcm = lcm * arg / gcd(arg,lcm)
	return lcm

def main():
	fi = fileinput.input()

	ntests = int(fi.readline())

	for test in range(ntests):

		nbandits = int(fi.readline())
		bandits = [int(x)-1 for x in fi.readline().strip().split(" ")]
		used = [False] * len(bandits)

		cycles = []
		for idx,start in enumerate(bandits):
			if used[idx]:
				continue

			nidx = idx
			cycle_len = 0
			while True:
				used[nidx] = True
				cycle_len += 1
				nidx = bandits[nidx]
				if(nidx == idx):
					cycles.append(cycle_len)
					break
		print lcm(cycles) % ((10**9) + 7)


if __name__ == '__main__':
	main()