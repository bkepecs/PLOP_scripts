import matplotlib.pyplot as plt
import sys
import numpy as np

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
y_pos = np.arange(len(seeds))
plt.barh(y_pos, energies)
#plt.yticks(y_pos, seeds, size='xx-small', stretch='ultra-expanded')
plt.ylabel('Seed')
plt.xlabel('Energy')
plt.title('Side Chain Addition Analysis')
top = max(energies)
bottom = min(energies)
plt.xlim(top, bottom)
#plt.show()
plt.savefig(str(sys.argv[1].split('_')[1]) + 'seeds.png')
