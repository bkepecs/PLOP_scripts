import sys

# open the file, read results into list of lines, slice out first line
with open(sys.argv[1], 'r') as rf:
    results = rf.readlines()
results = results[1:]

# make three lists with seeds, iteration numbers, energies
seeds = []
iterNumbers = []
energies = []

for line in results:
    data = line.split()
    seeds.append(data[0])
    iterNumbers.append(int(data[1]))
    energies.append(float(data[8]))

energies, seeds = (list(t) for t in zip(*sorted(zip(energies, seeds))))
for i in range(0, len(energies)):
	print(str(energies[i]) + '\t\t' + str(seeds[i]))
