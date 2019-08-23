import argparse
import os
import numpy
import sys

RMSD_CUTOFF = 2.0

def reportDevRanks(all, nativeLoops):
	lines = None
	with open(all, 'r') as f:
		lines = f.readlines()[1:]

	# Make a tmp file containing standard deviations
	currentPattern = lines[0].split()[1]
	patternEnergies = []
	devs = []

	for line in lines:
		terms = line.split()
		newPattern = terms[1]
		if newPattern == currentPattern:
			# Building a list of energies for one pattern
			patternEnergies.append(float(terms[2]))
		else:
			# Encountered new pattern
			# Store the standard deviation for the old pattern
			a = numpy.asarray(patternEnergies)
			stdev = numpy.std(a)
			double = [currentPattern, stdev]
			devs.append(double)
			# Clear the list for new pattern
			del patternEnergies[:]
			# Reset the pattern
			currentPattern = newPattern
			
			# Start building new list
			patternEnergies.append(float(terms[2]))
	
	# Take care of last pattern
	a = numpy.asarray(patternEnergies)
	double = [currentPattern, numpy.std(a)]
	devs.append(double)
	devs.sort(key=lambda x: x[1])

	
	tmp = 'v92.finalResult_tmp'
	if os.path.exists(tmp):
		os.remove(tmp)
	with open(tmp, 'w+') as f:
		for i in range(0, len(devs)):
			f.write(devs[i][0].ljust(12) + str(devs[i][1]).ljust(12) + '\n')

	lines = None
	with open(tmp, 'r') as f:
		lines = f.readlines()
	os.remove(tmp)

	ranks = []
	rank = 1
	
	for line in lines:
		terms = line.split()
		pattern = terms[0]
		if pattern in nativeLoops:
			ranks.append([pattern, rank])
		rank+=1
	tot = len(lines)

	return ranks, tot
	

def reportMaxRanks(all, nativeLoops):
	lines = None
	with open(all, 'r') as f:
		lines = f.readlines()[1:]

	# Make a tmp file containing max energies
	currentPattern = lines[0].split()[1]
	patternEnergies = []
	maxEnergies = []

	for line in lines:
		terms = line.split()
		newPattern = terms[1]
		if newPattern == currentPattern:
			# Building a list of energies for one pattern
			patternEnergies.append([currentPattern, float(terms[2])])
		else:
			# Encountered new pattern
			# Store the max for the old pattern
			maxEnergies.append(max(patternEnergies, key=lambda x: x[1]))
			# Clear the list for new pattern
			del patternEnergies[:]
			# Reset the pattern
			currentPattern = newPattern
			
			# Start building new list
			patternEnergies.append([currentPattern, float(terms[2])])
	maxEnergies.append(max(patternEnergies, key=lambda x: x[1]))
	maxEnergies.sort(key=lambda x: x[1])

	tmp = 'v92.finalResult_tmp'
	if os.path.exists(tmp):
		os.remove(tmp)
	with open(tmp, 'w+') as f:
		for i in range(0, len(maxEnergies)):
			f.write(maxEnergies[i][0].ljust(12) + str(maxEnergies[i][1]).ljust(12) + '\n')

	lines = None
	with open(tmp, 'r') as f:
		lines = f.readlines()
	os.remove(tmp)

	ranks = []
	rank = 1
	
	for line in lines:
		terms = line.split()
		pattern = terms[0]
		if pattern in nativeLoops:
			ranks.append([pattern, rank])
		rank+=1
	tot = len(lines)

	return ranks, tot
	

def reportMinRanks(min, nativeLoops):
	lines = None
	with open(min, 'r') as f:
		lines = f.readlines()[1:]
	
	ranks = []
	rank = 1
	for line in lines:
		terms = line.split()
		pattern = terms[1]
		if pattern in nativeLoops:
			ranks.append([pattern, rank])
		rank+=1
	tot = len(lines)

	return ranks, tot

# Returns list of native-like loops
def pickTargets(reference, goal):
	lines = None
	with open(reference, 'r') as f:
		lines = f.readlines()[1:]
	nativeLoops = []
	i = 0
	for line in lines:
		terms = line.split()
		if float(terms[8]) < RMSD_CUTOFF:
			nativeLoops.append(terms[1])
			i+=1
		if i == goal:
			break
	return nativeLoops

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('screenType', type=str)
	args = parser.parse_args()

	# Reference file containing canon loops
	reference = 'v92.finalResult_ref' 
	# New results from log that you want to screen
	min = 'v92.finalResult'
	# New results (all) from stdout that you want to screen
	all = 'v92.finalResult_all' 
	
	print('Searching for v92.finalResult_ref, v92.finalResult, v92.finalResult_all...')
	if os.path.exists('v92.finalResult_ref') and os.path.exists(
		'v92.finalResult') and os.path.exists('v92.finalResult_all'):
		print('All files found.')
	else:
		sys.exit('Files missing.')

	# Number of native-like loops that you want to keep
	goal = 10 
	# Returns list of native-like loops
	nativeLoops = pickTargets(reference, goal)
	
	if args.screenType == 'min':
		# Returns ranks of native-like loops from screen, according to 
		# minimum iteration energies
		minRanks, tot = reportMinRanks(min, nativeLoops)
		
		print('Ranking based on minimum energy of all iterations.\n')
		print('PATTERN'.ljust(12) + 'RANK (out of %s)' % tot)
		for i in range(0, len(minRanks)):
			print(minRanks[i][0].ljust(12) + str(minRanks[i][1]).ljust(12))

	elif args.screenType == 'max':
		# Returns ranks of native-like loops from screen, all iterations 
		maxRanks, tot = reportMaxRanks(all, nativeLoops)
		
		print('Ranking based on maximum energy of all iterations.\n')
		print('PATTERN'.ljust(12) + 'RANK (out of %s)' % tot)
		for i in range(0, len(maxRanks)):
			print(maxRanks[i][0].ljust(12) + str(maxRanks[i][1]).ljust(12))
	elif args.screenType == 'dev':
		devRanks, tot = reportDevRanks(all, nativeLoops)

		print('Ranking based on standard deviation of energies from all iterations.\n')
		print('PATTERN'.ljust(12) + 'RANK (out of %s)' % tot)
		for i in range(0, len(devRanks)):
			print(devRanks[i][0].ljust(12) + str(devRanks[i][1]).ljust(12))
		


if __name__ == '__main__':
	main()
