import os
import sys
import shutil
import argparse
import random

STEPSIZE = 1

# Ben's script to generate confile with ranges of seeds and iteration numbers.
# Proper way to call: ./generateConfiles.py 3 1000, e.g

# Function to edit a control file's seed and iteration number
def createSubjob(seed, iter, pattern):
	cwd = os.getcwd()
	fileData = None
	conFile = './v92_p' + pattern[0] + '.con'
	with open(conFile, 'r') as f:
		fileData = f.read()
	
	# editing
	newData = fileData.replace('SEEDKEY', seed)
	newData = newData.replace('ITERKEY1', iter)
	newData = newData.replace('ITERKEY2', iter)

	# creating subjob directories
	subDirName = os.path.join(cwd, 'subJobs', str(seed) + '_' + str(iter))
	os.makedirs(subDirName)
	
	# adding new control files to subjob directories
	subConName = os.path.join(subDirName, 'v92_' + str(seed) + '_' + str(iter) + '.con')
	with open(subConName, 'w') as f:
		f.write(newData)

	# symbolically linking all files in parent directory to subjob directory
	for filename in os.listdir(cwd):
		os.symlink(os.path.join(cwd, filename), os.path.join(cwd, subDirName, filename))

def makePatternFolder(pattern):
	cwd = os.getcwd()
	fileData = None
	with open('./v92.con', 'r') as conFile:
		fileData = conFile.read()
	
	newData = fileData.replace('PATTERN', pattern[0])
	newData = newData.replace('START', pattern[1])
	newData = newData.replace('END', pattern[2])

	patternFolder = os.path.join(cwd, 'patterns', 'p' + pattern[0])
	os.makedirs(patternFolder)
	patternCon = os.path.join(patternFolder, 'v92_p' + pattern[0] + '.con')
	with open(patternCon, 'w') as conFile:
		conFile.write(newData)
	
	for file in os.listdir(cwd):
		os.symlink(os.path.join(cwd, file), os.path.join(patternFolder, file))
	
	return patternFolder

def getPatterns():
	with open('pattern_partition.info', 'r') as f:
		lines = f.readlines()
	lines = lines[1:]
	patterns = []
	for line in lines:
		patterns.append(line.split())
	return patterns

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('seed_number', type=int)
	parser.add_argument('iter_start', type=int)
	parser.add_argument('iter_end', type=int)
	args = parser.parse_args()
	
	raw_input('Confirm?')
	print('Deleting old folder...')
	
	if os.path.exists('./patterns'):
		shutil.rmtree('./patterns')
	print('Done.')

	print('Generating seeds...')
	seedList = []
	for i in range(args.seed_number):
		seed = random.randint(11, 10000000)
		seedList.append(seed)
	
	cwd = os.getcwd()
	print('Reading patterns...')
	patterns = getPatterns()
	for pattern in patterns:
		print('Creating folder for pattern %s...' % pattern[0])
		patternFolder = makePatternFolder(pattern)
		os.chdir(patternFolder)
		
		path = os.getcwd()

		if os.path.exists('./subJobs'):
			shutil.rmtree('./subJobs')
		
		for seed in seedList:
			for iter in range(args.iter_start, args.iter_end + STEPSIZE, STEPSIZE):
				createSubjob(str(seed), str(iter), pattern)
		
		os.chdir(cwd)

if __name__ == "__main__":main()
