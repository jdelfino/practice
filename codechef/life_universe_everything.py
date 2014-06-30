import fileinput

''' http://www.codechef.com/problems/TEST '''

def main():
	for line in fileinput.input():
		if line.strip() == '42':
			return
		print line.strip()

if __name__ == '__main__':
	main()