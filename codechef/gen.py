from random import randint

def main():
	T = 25
	#T = randint(1, 25)

	print T
	for i in range(T):
		N = 10000
		Q = 10000
		#N = randint(1, 10000)
		#Q = randint(1, 10000)
		print N
		print ' '.join([str(randint(1, 10**6)) for x in range(N)])
		print Q
		for j in range(Q):
			#tp = randint(0,1)
 			tp = 0
			if tp == 0:
				print "0 %s %s" % (randint(1, N), randint(1,N))
			else:
				print "1 %s" %  (randint(1,N))

if __name__ == '__main__':
	main()