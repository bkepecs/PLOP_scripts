# Version that doesn't require specified bounds

import os
import argparse
from operator import itemgetter, attrgetter

def generateFinalResults():
	
	cwd = os.getcwd()
	logFileName = 'v92.log'
	finalRes = []
	titleRes = ''

	for subJob in os.listdir(os.path.join(cwd, 'subJobs')):
		os.chdir(os.path.join(cwd, 'subJobs', subJob))
		subConFile = 'v92_' + subJob + '.con'
		seed = None
		iter = None
		with open(subConFile, 'r') as f:
			con_lines = f.readlines()
		for line in con_lines:
			if 'random seed' in line:
				seedLine = line.split()
				seed = seedLine[2]
			elif ('side1' in line) and ('iterations' in line):
				iterLine = line.split()
				iter = iterLine[6]

		# If the subjob has STARTED but not FINISHED
		if os.path.isfile(logFileName) and not os.path.islink('4KUZ_localsamp.maegz'):
			markIdx = -1
			with open(logFileName, 'r') as logFile:
				log_lines = logFile.readlines()
			for lineIdx in range(len(log_lines)):
				if 'ROT FREQ ' in log_lines[lineIdx]:
					rfs = str(round(float(log_lines[lineIdx].split()[2]),2)).zfill(5)
				if 'FINAL RESULTS' in log_lines[lineIdx]:
					markIdx = lineIdx + 3 # Go to the starting row of results
					titleRes = log_lines[lineIdx+2]
					titleRes = titleRes.replace('INDEX', 'SEED')
					titleRes = titleRes.replace('IPATTERN', 'ITERNUMBER')				
					idx = titleRes.find('PE_HBOND')
					titleRes = titleRes[:idx] + '    RFS        ' + titleRes[idx:] 
					break
			if markIdx != -1:
				for lineIdx in range(markIdx, len(log_lines)):
					lineElements = log_lines[lineIdx].split()
					print(lineElements)
					if len(lineElements) <= 7 or lineElements[0][0] < '0' or lineElements[0][0] > '9':
						break
					elif lineElements[7][1] > '0' and lineElements[7][1] < '9' and float(lineElements[7]) < 999995:
						lineElements[0] = int(seed)
						lineElements[1] = int(iter)
						lineElements.insert(3, rfs)
						finalRes.append(lineElements)
	os.chdir(cwd)
	print("Len og finalRes:", len(finalRes))
	print(finalRes)
	finalRes = sorted(finalRes, key=itemgetter(0,1))
	for res in finalRes:
		res[0] = str(res[0])
		res[1] = str(res[1])
	finalResFile = 'v92.finalResult'
	with open(finalResFile, 'w') as fResF:
		fResF.write(titleRes)
		for res in finalRes:
			print("res:", res)

			tmpStr = "{:10} {:12} {:12}".format(res[0], res[1], res[2])
			tmpStr += '         '.join(res[3:]) + '\n'
			print(tmpStr)
			fResF.write(tmpStr)

def main():
	generateFinalResults()	

if __name__ == '__main__':
	main()
