import fileinput

def main():
	fi = fileinput.input()

	N, K, P = [int(x) for x in fi.readline().strip().split(" ")]

	frogs = [int(x) for x in fi.readline().strip().split(" ")]

	sorted_frogs = sorted(frogs)

	cidx = 0
	clusters = {sorted_frogs[0]:cidx}
	for i in range(1, len(sorted_frogs)):
		if (sorted_frogs[i] - sorted_frogs[i-1]) > K:
			cidx += 1

		clusters[sorted_frogs[i]] = cidx

	for linenum in range(P):
		first, second = [int(x)-1 for x in fi.readline().strip().split(" ")]

		if clusters[frogs[first]] == clusters[frogs[second]]:
			print "Yes"
		else:
			print "No"
		
		
if __name__ == '__main__':
	main()