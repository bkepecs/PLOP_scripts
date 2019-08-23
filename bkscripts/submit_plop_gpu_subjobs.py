import os
import sys
import subprocess32

def main():
	'''
	split_loops = '. ~/.bashrc split_loops_for_gpu %s %s' % (sys.argv[1], sys.argv[2])
	subprocess32.Popen(['bash', '-c', split_loops])
	'''
	
	os.chdir('subJobs')
	cwd = os.getcwd()
	for subjob in os.listdir('./'):
		os.chdir(subjob)
		jobConStr = '. ~/.bashrc; submit_plop_gpu v92_' + subjob + '.con > v92.stdout &'
		print(jobConStr)
		subprocess32.Popen(['bash', '-c', jobConStr])
		os.chdir(cwd)
	
if __name__ == '__main__':
	main()
