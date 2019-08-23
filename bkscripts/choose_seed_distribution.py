import os
from random import sample
import sys

def choose(seedNumber):
	with open('v92.finalResult', 'r') as f:
		lines = f.readlines()
	title = lines[0]
	lines = lines[1:]
	subLines = sample(lines, seedNumber)
	with open('v92.finalResult_' + str(seedNumber), 'w+') as f:
		f.write(title)
		for line in subLines:
			f.write(line)

def main():
	seedNumber = int(sys.argv[1])
	choose(seedNumber)

if __name__ == '__main__':
	main()
