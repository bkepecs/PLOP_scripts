import matplotlib.pyplot as plt
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
    seeds.append(int(data[0]))
    iterNumbers.append(int(data[1]))
    energies.append(float(data[8]))

# find indices of seed changes and store in seedIndexList
index = 0
currentSeed = None
seedIndexList = []
for seed in seeds:
    if seed != currentSeed:
        currentSeed = seed
        seedIndexList.append(index)
    index += 1
seedIndexList.append(index)

for number in range(0, len(seedIndexList) - 1):
    seed = seeds[seedIndexList[number]]
    subIterNumbers = iterNumbers[seedIndexList[number]:seedIndexList[number+1]]
    subEnergies = energies[seedIndexList[number]:seedIndexList[number+1]]

    print(seed)
    print(subIterNumbers)
    print(subEnergies)

    plt.plot(subIterNumbers, subEnergies, label= str(seed), marker='o')

plt.xlabel('Iteration Number')
plt.ylabel('Energy')
plt.title('Side Chain Addition Analysis')
plt.legend()
plt.show()
