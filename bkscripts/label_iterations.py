#! /usr/bin/python2

with open('./v92.log', 'r') as rf:
	lines = rf.readlines()
newlines = []
iterNumber = 1
for line in lines:
	if 'Randomizing side chain' in line:
		label = 'ITERATION NUMBER ' + str(iterNumber) + '\n'
		newlines.append(label)
		newlines.append(line)
		iterNumber += 1
	else:
		newlines.append(line)

with open('./v92_labeled.log', 'w') as rf:
	rf.writelines(newlines)
