import os
import timeit
def readFile(fileName):

	print('Python PLaying')
	os.system('python3 homework3.py')
	print('Java PLaying')
	os.system('python3 homework3.py')

	
	
	
	
	
	
	
	


start = timeit.default_timer()

try:
	i=0
	while i!=500:
		readFile("./input.txt")
		i+=1
	print('Time for Game',timeit.default_timer()-start)
except:
	print('endded')