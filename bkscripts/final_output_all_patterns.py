# Version that doesn't require specified bounds

import os
import argparse
from operator import itemgetter, attrgetter

def generateFinalResults():
	
	cwd = os.getcwd()
	logFileName = 'v92.log'
	finalRes = []
	titleRes = ''
	patterns = os.path.join(cwd, 'patterns')
	for pattern in os.listdir(patterns):
		patternN = pattern[1:]
		subJobs = os.path.join(patterns, pattern, 'subJobs')
		for subJob in os.listdir(subJobs):
			os.chdir(os.path.join(subJobs, subJob))
			subJobName = subJob.split('_')
			seed = subJobName[0]
			iter = subJobName[1]

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
						titleTerms = titleRes.split()
						titleTerms.insert(2, 'SEED')
						titleTerms.insert(3, 'ITER_NUMBER')
						titleTerms.insert(4, 'RFS')
						tmp = titleTerms[4]
						titleTerms[4] = titleTerms[10]
						titleTerms[10] = tmp
						break
				if markIdx != -1:
					for lineIdx in range(markIdx, len(log_lines)):
						lineElements = log_lines[lineIdx].split()
						print(lineElements)
						if len(lineElements) <= 7 or lineElements[0][0] < '0' or lineElements[0][0] > '9':
							break
						elif lineElements[7][1] > '0' and lineElements[7][1] < '9' and float(lineElements[7]) < 999995:
							lineElements[1] = int(lineElements[1])
							lineElements.insert(2, str(seed))
							lineElements.insert(3, int(iter))
							lineElements.insert(4, rfs)
							tmp  = lineElements[4]
							lineElements[4] = lineElements[10]
							lineElements[10] = tmp
							lineElements[4] = float(lineElements[4])
							finalRes.append(lineElements)
	os.chdir(cwd)
	print(finalRes)
	finalRes = sorted(finalRes, key=itemgetter(4))
	for res in finalRes:
		res[1] = str(res[1])
		res[3] = str(res[3])
	finalResFile = 'v92.finalResult'
	title = ''
	for term in titleTerms:
		title = title + term.ljust(12)
			
	with open(finalResFile, 'w') as fResF:
		fResF.write(title + '\n')
		for res in finalRes:
			x1 = ''
			for thing in res:
				x1 = x1 + str(thing).ljust(12)
			fResF.write(x1 + '\n')

def main():
	generateFinalResults()	

if __name__ == '__main__':
	main()
