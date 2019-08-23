import argparse
from operator import itemgetter
import math

def reportCutoffs1(ranks, seedN):
	# 9/10 cutoffs, single seeds
	cutoffs1 = []
	i = 0
	for seed in range(0, seedN):
		currentSeed = ranks[i][0]
		seedRanks = []
		for j in range(i, len(ranks)):
			rank = ranks[i]
			if not rank[0] == currentSeed:
				break
			else:
				seedRanks.append(int(rank[2]))
			i += 1
		seedRanks = sorted(seedRanks)
		cutoffs1.append(seedRanks[8])

	return cutoffs1

def reportCutoff234(ranks, seedN):
	seeds = []
	i = 0
	for seed in range(0, seedN):
		currentSeed = ranks[i][0]
		seedRanks = []
		for j in range(i, len(ranks)):
			rank = ranks[i]
			if not rank[0] == currentSeed:
				break
			else:
				seedRanks.append(rank[2])
			i += 1
		seeds.append(seedRanks)
	minRanks = []
	avgRanks = []
	rangeRanks = []
	for i in range(0, len(seeds[0])):
		currentPatternRanks = []
		for seedRanks in seeds:
			currentPatternRanks.append(int(seedRanks[i]))
		minRank = min(currentPatternRanks)
		minRanks.append(minRank)
		avgRank = int(math.ceil(sum(currentPatternRanks)/len(currentPatternRanks)))
		avgRanks.append(avgRank)
		rangeRank = max(currentPatternRanks) - min(currentPatternRanks)
		rangeRanks.append(rangeRank)
	
	minRanks = sorted(minRanks)
	avgRanks = sorted(avgRanks)
	rangeRanks = sorted(rangeRanks)
	cutoff2 = minRanks[8]
	cutoff3 = avgRanks[8]
	cutoff4 = rangeRanks[8]

	return cutoff2, cutoff3, cutoff4

def reportCutoff56(energies, seedN, screen):
	seeds = []
	i = 0
	for seed in range(0, seedN):
		currentSeed = energies[i][0]
		seedEnergies = []
		for j in range(i, len(energies)):
			energy = energies[i]
			if not energy[0] == currentSeed:
				break
			else:
				seedEnergies.append(energy[2])
			i += 1
		seeds.append(seedEnergies)
	avgEnergies = []
	rangeEnergies = []
	for i in range(0, len(seeds[0])):
		currentPatternEnergies = []
		for seedEnergies in seeds:
			currentPatternEnergies.append(float(seedEnergies[i]))
		avgEnergy = sum(currentPatternEnergies)/len(currentPatternEnergies)
		avgEnergies.append(avgEnergy)
		avgRanks = energiesToRanks(avgEnergies, screen)
		rangeEnergy = max(currentPatternEnergies) - min(currentPatternEnergies)
		rangeEnergies.append(rangeEnergy)
		rangeRanks = energiesToRanks(rangeEnergies, screen)

	avgRanks = sorted(avgRanks)
	rangeRanks = sorted(rangeRanks)
	cutoff5 = avgRanks[8]
	cutoff6 = rangeRanks[8]

	return cutoff5, cutoff6

def energiesToRanks(energies, screen):
	with open(screen, 'r') as f:
		lines = f.readlines()[1:]
	ranks = []
	for energy in energies:
		screenEnergies = []
		for line in lines:
			terms = line.split()
			screenEnergies.append(float(terms[4]))
		screenEnergies.append(energy)
		screenEnergies = sorted(screenEnergies)
		for i in range(0,len(screenEnergies)):
			if screenEnergies[i] == energy:
				ranks.append(i)
	
	return ranks

def printRanks(ranks, tot):
	print('Seed'.ljust(10) + 'Pattern'.ljust(10) + 'Rank (out of %s)' % tot)
	for rank in ranks:
		print(rank[0].ljust(10) + rank[1].ljust(10) + str(rank[2]).ljust(10))

def reportEnergies(screen, nativeLoops):
	lines = None
	with open(screen, 'r') as f:
		lines = f.readlines()[1:]
	energies = []
	seeds = []
	i = 1
	for line in lines:
		terms = line.split()
		seed = terms[2]
		if seed not in seeds:
			seeds.append(seed)
		pattern = terms[1]
		energy = float(terms[4])
		if pattern in nativeLoops:
			energies.append([seed,pattern,energy])
		i += 1
	tot = i
	return sorted(energies, key=itemgetter(0,1)), tot, len(seeds)

def reportRanks(screen, nativeLoops):
	lines = None
	with open(screen, 'r') as f2:
		lines = f2.readlines()[1:]
	ranks = []
	seeds = []
	i = 1
	for line in lines:
		terms = line.split()
		seed = terms[2]
		if seed not in seeds:
			seeds.append(seed)
		pattern = terms[1]
		if pattern in nativeLoops:
			ranks.append([seed,pattern,i])
		i += 1
	tot = i
	return sorted(ranks, key=itemgetter(0,1)), tot, len(seeds)

def pickTargets(reference, goal):
	lines = None
	with open(reference, 'r') as f1:
		lines = f1.readlines()[1:]
	nativeLoops = []
	i = 0
	for line in lines:
		terms = line.split()
		if float(terms[8]) < 2.0:
			nativeLoops.append(terms[1])
			i += 1
		if i == goal:
			break
	return nativeLoops

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('reference', type=str)
	parser.add_argument('screen', type=str)
	args = parser.parse_args()

	goal = 10
	nativeLoops = pickTargets(args.reference, goal)
	ranks, tot, seedN = reportRanks(args.screen, nativeLoops)
	
	# In case any jobs died
	while len(ranks) < 10*seedN:
		goal += 1
		nativeLoops = pickTargets(args.reference, goal)
		ranks, tot, seedN = reportRanks(args.screen, nativeLoops)

	printRanks(ranks, tot)

	cutoffs1 = reportCutoffs1(ranks, seedN)
	
	print('\nCutoffs to include 9/10 best:')
	for cutoff in cutoffs1:
		print(cutoff)
	
	cutoff2, cutoff3, cutoff4 = reportCutoff234(ranks, seedN)
	print('\nCutoff to include 9/10 best using minimum ranking:')
	print(cutoff2)
	print('\nCutoff to include 9/10 best using average ranking:')
	print(cutoff3)
	print('\nCutoff to include 9/10 best using rank range:')
	print(cutoff4)

	# Energy cutoffs
	goal = 10
	energies, tot, seedN = reportEnergies(args.screen, nativeLoops)
	
	# In case any jobs died
	while len(energies) < 10*seedN:
		goal += 1
		nativeLoops = pickTargets(args.reference, goal)
		energies, tot, seedN = reportRanks(args.screen, nativeLoops)
	
	cutoff5, cutoff6 = reportCutoff56(energies, seedN, args.screen)
	print('\nCutoffs to include 9/10 best using average energy:')
	print(cutoff5)
	print('\nCutoff to include 9/10 best using range of energies:')
	print(cutoff6)

if __name__ == '__main__':
	main()
