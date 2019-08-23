import os
import sys
import shutil
import argparse
import random

STEPSIZE = 200
SEEDNUMBER = 6

# Ben's script to generate confile with ranges of seeds and iteration numbers.
# Proper way to call: ./generateConfiles.py 3 1000, e.g

# Function to edit a control file's seed and iteration number
def createSubjob(seedInput, iterInput1, iterInput2, index):
	
	cwd = os.getcwd()
	fileData = None
	with open('./v92.con', 'r') as conFile:
		fileData = conFile.read()
	
	# editing
	newData = fileData.replace('SEEDKEY', seedInput)
	newData = newData.replace('ITERKEY1', iterInput1)
	newData = newData.replace('ITERKEY2', iterInput2)
	
	# creating subjob directories
	subDirName = os.path.join(cwd, 'subJobs', seedInput + '_' + str(index))
	os.makedirs(subDirName)
	
	# adding new control files to subjob directories
	subConName = os.path.join(cwd,'v92_' + seedInput + '_' + str(index) + '.con')
	with open(subConName, 'w') as conFile:
		conFile.write(newData)
	shutil.move(subConName, subDirName + '/v92_' + seedInput + '_' + str(index) + '.con')

	# symbolically linking all files in parent directory to subjob directory
	for filename in os.listdir(cwd):
		os.symlink(os.path.join(cwd, filename), os.path.join(cwd, 'subJobs', seedInput + '_' + str(index), filename))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('job_mode', type=int)
	parser.add_argument('seed_start', type=int)
	parser.add_argument('seed_end', type=int)
	parser.add_argument('iter_start', type=int)
	parser.add_argument('iter_end', type=int)
	args = parser.parse_args()
	
	if os.path.exists('./subJobs'):
		shutil.rmtree('./subJobs')

	if args.job_mode == 0:
		for seed in range(args.seed_start, args.seed_end + 1):
			index = 1
			for iter in range(args.iter_start, args.iter_end + STEPSIZE, STEPSIZE):
				createSubjob(str(seed), str(iter), str(iter), str(index))
				index += 1
	elif args.job_mode == 1:
		seedList = []
		for i in range(SEEDNUMBER):
			seed = random.randint(11, 10000000)
			seedList.append(seed)
		for seed in seedList:
			index = 1
			for iter in range(args.iter_start, args.iter_end + STEPSIZE, STEPSIZE):
				createSubjob(str(seed), str(iter), str(iter), str(iter))
				index += 1
			
if __name__ == "__main__":main()
