import os

def checkFolders():
	cwd = os.getcwd()
	for subJob in os.listdir(os.path.join(cwd, 'subJobs')):
		os.chdir(os.path.join(cwd, 'subJobs', subJob))	
		print(subJob + ': '),
		#cwd = os.getcwd()
		if os.path.isfile('plop.stdout') and not os.path.islink('4KUZ_localsamp.maegz'):
			print('done')
		else:
			print('')
		os.chdir(cwd)

def main():
	checkFolders()	

if __name__ == '__main__':
	main()
