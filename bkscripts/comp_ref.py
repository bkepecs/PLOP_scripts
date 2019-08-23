import os
from schrodinger import structure
from schrodinger.structutils import rmsd
from schrodinger.structutils.interactions import hbond
from schrodinger.structutils.interactions import pi
from schrodinger.structutils.interactions import salt_bridge
from schrodinger.structutils import analyze
import copy
import sys
import difflib

ALLINDICES_asl = 'all'
LOOPENVINDICES_asl = 'fillres within 4.0 ((res.num 97-109) AND ((chain.name H)) )'
#Just loop with sidechains
#Just loop without sidechains

NONLOOPINDICES_asl = '((all) AND NOT ((fillres within 4 ((res.num 97-109) AND ((chain.name H)) ) ))) AND NOT (( sidechain ) )'

def rmsdRef():
	lines = []
	with open('v92.finalResult', 'r') as f:
		lines = f.readlines()[1:]
	seeds = []
	energies = []
	nativeRMSDs = []
	for line in lines:
		terms = line.split()
		seeds.append(int(terms[0]))
		energies.append(float(terms[8]))
		nativeRMSDs.append(terms[9])
	energies, seeds, nativeRMSDs = (list(t) for t in \
	zip(*sorted(zip(energies, seeds, nativeRMSDs))))

	cwd = os.getcwd()
	
	pattern = None
	with open('v92.con', 'r') as f:
		conLines = f.readlines()
	for line in conLines:
		if 'subjob_control' in line:
			terms = line.split()
			pattern = terms[2]
	
	structs = []
	for i in range(len(seeds)):
		for dir in os.listdir(os.path.join(cwd, 'subJobs')):
			if dir.split('_')[0] == str(seeds[i]):
				os.chdir(os.path.join(cwd, 'subJobs', dir))
				if 'plop.stdout' in os.listdir('.'):
					stName = '4KUZ-p' + str(pattern) + '-' + nativeRMSDs[i] + '_template.maegz'
					structs.append(next(structure.StructureReader(stName)))
				os.chdir(cwd)
	minStruct = copy.deepcopy(structs[0])
	
	ALLINDICES = analyze.evaluate_asl(minStruct, ALLINDICES_asl)
	LOOPENVINDICES = analyze.evaluate_asl(minStruct, LOOPENVINDICES_asl)
	NONLOOPINDICES = analyze.evaluate_asl(minStruct, NONLOOPINDICES_asl)

	rmsds = []
	for i in range(0, len(structs)):
		curStruct = structs[i]
		rmsd.superimpose(minStruct, NONLOOPINDICES, curStruct, NONLOOPINDICES)
		RMSD = rmsd.calculate_in_place_rmsd(minStruct,
			LOOPENVINDICES, curStruct, LOOPENVINDICES)
		rmsds.append(RMSD)
	
	# What about Hbond patterns?
	hbonds = []
	for i in range(0, len(structs)):
		curStruct = structs[i]
		hbonds.append(hbond.get_hydrogen_bonds(curStruct, LOOPENVINDICES))
	
	hbondIndices = []	
	for i in range(0, len(hbonds)):
		structIndices = []
		hbondIndices.append(structIndices)
		for j in range(0, len(hbonds[i])):
			pairIndices = []
			hbondIndices[i].append(pairIndices)
			for k in range(0, 2):
				hbondIndices[i][j].append(hbonds[i][j][k].index)
	
	min_hb_indices = copy.deepcopy(hbondIndices[0])
	hbond_overlaps = []
	for i in range(0, len(hbondIndices)):
		li1 = [tuple(lst) for lst in min_hb_indices]
		li2 = [tuple(lst) for lst in hbondIndices[i]]
		
		overlap = []
		for pair in li1:
			if pair in li2:
				overlap.append(pair)
		sm = difflib.SequenceMatcher(None, li1, li2)
		hbond_overlaps.append(round(sm.ratio(), 5))
	
	# What about salt bridge interactions?
	bridges = []
	for i in range(0, len(structs)):
		curStruct = structs[i]
		bridges.append(salt_bridge.get_salt_bridges(curStruct, LOOPENVINDICES))
	
	bridgeIndices = []	
	for i in range(0, len(bridges)):
		structIndices = []
		bridgeIndices.append(structIndices)
		for j in range(0, len(bridges[i])):
			pairIndices = []
			bridgeIndices[i].append(pairIndices)
			for k in range(0, 2):
				bridgeIndices[i][j].append(bridges[i][j][k].index)
	
	min_bridge_indices = copy.deepcopy(bridgeIndices[0])
	salt_bridge_overlaps = []
	for i in range(0, len(bridgeIndices)):
		li1 = [tuple(lst) for lst in min_bridge_indices]
		li2 = [tuple(lst) for lst in bridgeIndices[i]]
		
		overlap = []
		for pair in li1:
			if pair in li2:
				overlap.append(pair)
		sm = difflib.SequenceMatcher(None, li1, li2)
		salt_bridge_overlaps.append(round(sm.ratio(), 5))
	
	# Hydrophobic interactions


	print('SEED\t\tRMSD\t\tHBOND_OVERLAP\tSALTBR_OVERLAP\tENERGY')
	for i in range(0, len(rmsds)):
		print(str(seeds[i])+'\t\t'+str(round(rmsds[i], 3))+'\t\t'+
		str(hbond_overlaps[i]*100)+'\t\t'+str(salt_bridge_overlaps[i]*100)+
		'\t\t'+str(energies[i]))

def main():
	rmsdRef()

if __name__=='__main__':
	main()
