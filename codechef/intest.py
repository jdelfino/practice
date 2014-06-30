import fileinput

''' http://www.codechef.com/problems/TEST '''

def main():
	fi = fileinput.input()
	n, div = fi.readline().strip().split()
	div = int(div)

	count = 0

	for line in fi:
		if int(line) % div == 0:
			count = count + 1
	print count

if __name__ == '__main__':
	main()