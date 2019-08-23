import os
import shutil

def deleteSubjobs():
	cwd = os.getcwd()
	for subJob in os.listdir(os.path.join(cwd, 'subJobs')):
		path = os.path.join(cwd, 'subJobs', subJob)
		if os.path.isfile(os.path.join(path, 'plop.stdout')) \
			and not os.path.islink(os.path.join(path,'4KUZ_localsamp.maegz')):
			pass
		else:
			shutil.rmtree(path)

def main():
	deleteSubjobs()	

if __name__ == '__main__':
	main()
