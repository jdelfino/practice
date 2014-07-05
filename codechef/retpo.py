import fileinput

def main():
	fi = fileinput.input()
	ntests = int(fi.readline())

	for ntest in range(ntests):
		x,y = [int(x) for x in fi.readline().strip().split(" ")]
		posx = abs(x)
		posy = abs(y)
		sside = min(posx,posy)

		base = sside * 2 # get to (min(x,y), min(x,y)), facing east

		rem = posy - posx
		if posx > posy:
			base -= 1 # stop 1 short, facing north
			rem = posx - posy + 1

		base += rem * 2
		if rem % 2:
			base -= 1
		print base

if __name__ == '__main__':
	main()
