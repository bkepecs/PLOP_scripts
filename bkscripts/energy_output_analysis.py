import os
import numpy

##### Ben's program to identify energy term that fluctuates the most in log
##### file of subjobs.

def printList(lists):
	for list in lists:
		print(list)

def getCOVTerm(allCOVEnergies):
	stdevs = numpy.zeros((2,3))
	for i in range(0,2):
		for j in range(0,3):
			currentTerms = []
			for subEnergies in allCOVEnergies:
				currentTerms.append(subEnergies[i][j])
			stdevs[i][j] = numpy.std(currentTerms)
	print('\nThe stdevs of the COV terms are:')
	terms = [['COV_BOND','COV_ANGLE','COV_TOR'],
		 ['SGB_BOND','SGB_ANGLE','SGB_TOR']]
	printList(terms)
	printList(stdevs)
	maxStdev = numpy.amax(stdevs)
	maxIndices = numpy.where(stdevs == numpy.amax(stdevs))
	maxIndexList = list(zip(maxIndices[0], maxIndices[1]))
	energyTerm = terms[maxIndexList[0][0]][maxIndexList[0][1]]
	print('Within COV, ' + energyTerm + ' has the highest fluctuation.')
	# See if SGB_BOND and SGB_ANGLE/SGB_TOR are correlated
	print('\n##########################################')
	print('Are SGB_BOND and SGB_ANGLE/SGB_TOR negatively correlated?\n')
	sgb_bonds = []
	sgb_angles = []
	sgb_tors = []
	for subEnergies in allCOVEnergies:
		sgb_bonds.append(subEnergies[1][0])
		sgb_angles.append(subEnergies[1][1])
		sgb_tors.append(subEnergies[1][2])
	print('SGB_BOND vs SGB_ANGLE:')
	print(numpy.corrcoef(sgb_bonds, sgb_angles))
	print('SGB_BOND vs SGB_TOR:')
	print(numpy.corrcoef(sgb_bonds, sgb_tors))
	print('##########################################')
	
	return energyTerm

def getNBTerm(allNBEnergies):
	stdevs = numpy.zeros((4,3))
	for i in range(0,4):
		for j in range(0,3):
			currentTerms = []
			for subEnergies in allNBEnergies:
				currentTerms.append(subEnergies[i][j])
			stdevs[i][j] = numpy.std(currentTerms)
	print('\nThe stdevs of the NB terms are:')
	terms = [['LJ_14','LJ_SHORT','LJ_LONG'],
		 ['LIPO_14','LIPO_SHORT','LIPO_LONG'],
		 ['EL_14','EL_SHORT','EL_LONG'],
		 ['SGB_14','SGB_SHORT','SGB_LONG']]
	printList(terms)
	printList(stdevs)
	maxStdev = numpy.amax(stdevs)
	maxIndices = numpy.where(stdevs == numpy.amax(stdevs))
	maxIndexList = list(zip(maxIndices[0], maxIndices[1]))
	energyTerm = terms[maxIndexList[0][0]][maxIndexList[0][1]]
	print('Within NB, ' + energyTerm + ' has the highest fluctuation.')
	return energyTerm

def getOTHTerm(allOTHEnergies):
	stdevs = numpy.zeros((7,1))
	for i in range(0,7):
		for j in range(0,1):
			currentTerms = []
			for subEnergies in allOTHEnergies:
				currentTerms.append(subEnergies[i][j])
			stdevs[i][j] = numpy.std(currentTerms)
	print('\nThe stdevs of the OTHER terms are:')
	terms = [['SGB_SELF'],['NONPOLAR'],['PROT_COR'],['HBOND'],['PACKING'],['SELFCONT'],['ROT_FREQ']]
	print(terms)
	print(stdevs)
	maxStdev = numpy.amax(stdevs)
	maxIndices = numpy.where(stdevs == numpy.amax(stdevs))
	maxIndexList = list(zip(maxIndices[0], maxIndices[1]))
	energyTerm = terms[maxIndexList[0][0]][maxIndexList[0][1]]
	print('Within OTHER, ' + energyTerm + ' has the highest fluctuation.')
	return energyTerm

def getFlucTerm(energies):
	stdevs = []
	for i in range(0, 4):
		currentTerms = []
		for subEnergies in energies:
			currentTerms.append(subEnergies[i])
		stdevs.append(numpy.std(currentTerms))
	
	print('The stdevs of the 4 main terms are:')
	terms = [ 'COV_TOT', 'NB_TOT', 'OTHER', 'SGB_TOR' ]
	print(terms)
	print(stdevs)
	maxStdev = max(stdevs)
	maxIndex = stdevs.index(maxStdev)
	energyTerm = terms[maxIndex]
	print(energyTerm + ' has the highest fluctuation.')
	return energyTerm

def getSubEnergies():
	mainEnergies = []
	COVEnergies = numpy.zeros((2,3))
	NBEnergies = numpy.zeros((4,3))
	OTHEnergies = numpy.zeros((7,1))

	with open('v92.log', 'r') as f:
		lines = f.readlines()
	lineIndex = 1
	for line in lines:
		if 'FINAL RESULTS' in line:
			break
		lineIndex += 1

	# A lot of hardcoded numbers, but shld be simple to follow
	# Aggregates the 4 main energy terms
	i = 1
	while 'COVALENT' not in lines[lineIndex-i]:
		i += 1
	cov_tot_line = lines[lineIndex-i+4]
	cov_tot_terms = cov_tot_line.split()
	COV_TOT = float(cov_tot_terms[4])
	mainEnergies.append(COV_TOT)
	
	for j in reversed(range(i-3, i-1)):
		cov_line = lines[lineIndex-j]
		cov_line_terms = cov_line.split()
		for k in range(1, 4):
			COVEnergies[i-2-j][k-1] = float(cov_line_terms[k])
	
	i = 1
	while 'NONBONDED' not in lines[lineIndex-i]:
		i += 1
	nb_tot_line = lines[lineIndex-i+6]
	nb_tot_terms = nb_tot_line.split()
	NB_TOT = float(nb_tot_terms[4])
	mainEnergies.append(NB_TOT)
	
	for j in reversed(range(i-5, i-1)):
		nb_line = lines[lineIndex-j]
		nb_line_terms = nb_line.split()
		for k in range(1, 4):
			NBEnergies[i-2-j][k-1] = float(nb_line_terms[k])
	
	i = 1
	while 'OTHER:' not in lines[lineIndex-i]:
		i += 1
	OTHER = 0
	for j in range(i-7,i):
		other_line = lines[lineIndex-j]
		other_line_terms = other_line.split()
		set = {'SGB', 'PROT', 'ROT'}
		if other_line_terms[0] in set:
			OTHER += float(other_line_terms[2])
		else:
			OTHER += float(other_line_terms[1])
	mainEnergies.append(OTHER)
	
	for j in reversed(range(i-7,i)):
		other_line = lines[lineIndex-j]
		other_line_terms = other_line.split()
		set = {'SGB', 'PROT', 'ROT'}
		if other_line_terms[0] in set:
			OTHEnergies[i-1-j] = float(other_line_terms[2])
		else:
			OTHEnergies[i-1-j] = float(other_line_terms[1])
	
	i = 1
	while 'COVALENT' not in lines[lineIndex-i]:
		i += 1
	sgb_tor_line = lines[lineIndex-i+3]
	sgb_tor_terms = sgb_tor_line.split()
	SGB_TOR = float(sgb_tor_terms[3])
	mainEnergies.append(SGB_TOR)

	return mainEnergies, COVEnergies, NBEnergies, OTHEnergies

def getAllEnergies():
	cwd = os.getcwd()
	allMainEnergies = []
	allCOVEnergies = []
	allNBEnergies = []
	allOTHEnergies = []
	for subJob in os.listdir(os.path.join(cwd, 'subJobs')):
		os.chdir(os.path.join(cwd, 'subJobs', subJob))
		if os.path.isfile('v92.log') and not os.path.islink('4KUZ_localsamp.maegz'):
			mainEnergies, COVEnergies, NBEnergies, OTHEnergies = getSubEnergies()
			allMainEnergies.append(mainEnergies)
			allCOVEnergies.append(COVEnergies)
			allNBEnergies.append(NBEnergies)
			allOTHEnergies.append(OTHEnergies)

	os.chdir(cwd)
	return allMainEnergies, allCOVEnergies, allNBEnergies, allOTHEnergies

def main():
	allMainEnergies, allCOVEnergies, allNBEnergies, allOTHEnergies = getAllEnergies()
	energyTerm = getFlucTerm(allMainEnergies)
	getCOVTerm(allCOVEnergies)
	getNBTerm(allNBEnergies)
	getOTHTerm(allOTHEnergies)
	
if __name__=='__main__':
	main()
