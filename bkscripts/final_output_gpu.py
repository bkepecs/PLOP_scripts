import os

STEPNUMBER = 2

def processStdouts(indices, patterns):
	cwd = os.getcwd()
	stdout = 'v92.stdout'
	energies = []

	i = -1
	for subjob in os.listdir('subJobs'):
		jobDir = os.path.join(cwd, 'subJobs', subjob)
		stdoutPath = os.path.join(jobDir, 'v92.stdout')
		
		lines = None
		with open(stdoutPath, 'r') as f:
			lines = f.readlines()
		
		j = STEPNUMBER
		for line in lines:
			if '  subroutine' in line:
				if j != STEPNUMBER:
					j += 1
				elif j == STEPNUMBER:
					i+=1
					j = 1

			if 'PATH' in line and j == 1:
				terms = line.split()
				energy = float(terms[4])
				energies.append([indices[i], patterns[i], energy])

	return energies


def mapIndices(indices):
	patternLines = None
	with open('pattern_partition.info', 'r') as f:
		patternLines = f.readlines()[1:]
	triples = []
	for line in patternLines:
		triples.append(line.split())
	
	patterns = []
	for index in indices:
		for triple in triples:
			if index <= int(triple[2]) and index >= int(triple[1]):
				patterns.append(triple[0])
	
	return patterns

def processLogs():
	cwd = os.getcwd()
	logName = 'v92.log'
	energies = []
	rmsds = []
	indices = []

	for subjob in os.listdir('subJobs'):
		jobDir = os.path.join(cwd, 'subJobs', subjob)
		logPath = os.path.join(jobDir, 'v92.log')
		
		logLines = None
		with open(logPath, 'r') as f:
			logLines = f.readlines()
		
		i = 0
		for line in logLines:
			if 'Pass 2' in line:
				energyLine = logLines[i-2]
				energy = float(energyLine.split()[1])
				energies.append(energy)
				rmsdLine = logLines[i]
				rmsd = float(rmsdLine.split()[6])
				rmsds.append(rmsd)
				
				j = i
				indexFound = -1
				while(indexFound < 0):
					if 'Working on' in logLines[j]:
						indexFound = 1
						indexLine = logLines[j]
						index = int(indexLine.split()[4])
						indices.append(index)
					else:
						j-=1
			i+=1


	return indices, energies, rmsds

def main():
	indices, energies, rmsds = processLogs()
	patterns = mapIndices(indices)

	energies, indices, patterns, rmsds = (list(t) for t in zip(*sorted(zip(energies, indices, patterns, rmsds))))

	with open('v92.finalResult', 'w+') as f:
		f.write('INDEX'.ljust(12) + 'PATTERN'.ljust(12) + 
		'ENERGY'.ljust(12) + 'RMSD'.ljust(12) + '\n')
		for i in range(0, len(indices)):
			f.write(str(indices[i]).ljust(12) + str(patterns[i]).ljust(12) + 
			str(round(energies[i], 3)).ljust(12) + str(rmsds[i]).ljust(12) + '\n')


	allEnergies = processStdouts(indices, patterns)
	
	with open('./v92.finalResult_all', 'w+') as f:
		f.write('INDEX'.ljust(12) + 'PATTERN'.ljust(12) + 
		'ENERGY'.ljust(12) + '\n')
		for i in range(0, len(allEnergies)):
			f.write(str(allEnergies[i][0]).ljust(12) + str(allEnergies[i][1]).ljust(12) +
			str(round(allEnergies[i][2], 3)).ljust(12) + '\n')
	
if __name__ == '__main__':
	main()
