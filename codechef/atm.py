import fileinput

''' # http://www.codechef.com/problems/HS08TEST '''

def main():
	line = fileinput.input().readline()
	withdraw, balance = line.split()
	withdraw = int(withdraw)
	balance = float(balance)

	if (withdraw % 5) or (withdraw + .5) > balance:
		print balance
	else:
		print balance - withdraw - .5

if __name__ == '__main__':
	main()