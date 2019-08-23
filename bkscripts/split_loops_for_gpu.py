import os
import math
import argparse
import shutil

PARTITION = 100

def generateSubFolders(loops, iter_number):
	cwd = os.getcwd()
	
	conData = None
	with open('./v92.con', 'r') as f:
		conData = f.read()
	
	newData = conData.replace('ITERKEY1', str(iter_number))
	newData = newData.replace('ITERKEY2', str(iter_number))

	folderNumber = int(math.ceil(float(len(loops))/PARTITION))
	print(str(folderNumber) + ' subfolders.')
	for i in range(0, folderNumber):
		subPath = os.path.join(cwd, 'subJobs', str(i))
		os.makedirs(subPath)
		
		loopList = None
		if i < folderNumber-1:
			loopList = loops[i*PARTITION:i*PARTITION+PARTITION]
			loopRange = str(i*PARTITION) + '_' + str(i*PARTITION+(PARTITION-1))
		else:
			loopList = loops[i*PARTITION:len(loops)]
			loopRange = str(i*PARTITION) + '_' + str(len(loops)-1)

		loopFile = os.path.join(subPath, 'looplist_' + loopRange)
		with open(loopFile, 'w+') as f1:
			f1.writelines(loopList)

		new2Data = newData.replace('LOOPFILE', 'looplist_' + loopRange)
		new2Data = new2Data.replace('LOOPNUMBER', str(len(loopList)))

		subCon = os.path.join(subPath, 'v92_' + str(i) + '.con')
		with open(subCon, 'w+') as f3:
			f3.write(new2Data)

		for file in os.listdir(cwd):
			if file != 'v92.stdout' and file != 'v92.log':
				os.symlink(os.path.join(cwd, file), os.path.join(subPath, file))


def getLoops(loop_file):
	with open(loop_file, 'r') as f:
		loops = f.readlines()
	
	return loops

def main():
	cwd = os.getcwd()

	parser = argparse.ArgumentParser()
	parser.add_argument('loop_file', type=str)
	parser.add_argument('iter_number', type=int)
	args = parser.parse_args()

	raw_input('Confirm?')
	print('Deleting old folder...')
	if os.path.exists('./subJobs'):
		shutil.rmtree('./subJobs')
	print('Done.')

	os.makedirs('subJobs')
	
	loops = getLoops(args.loop_file)
	
	generateSubFolders(loops, args.iter_number)
	
	os.chdir(cwd)

if __name__ == '__main__':
	main()
