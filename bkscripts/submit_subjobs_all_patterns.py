# Ben's modified version of submission script for pre-generated confiles with
# ranges of seeds and iteration numbers.

import argparse
import os
import shutil
from schrodinger.job import queue, jobcontrol
from schrodinger.utils import subprocess as schrod_subporcess

'''
    This script should be executed under the PARENT directory.
    AIM: generate subjob folders and initiate them using jobDJ parallelization method.
    
    run_plop_job.py is called by this script, and gets executed under each SUBJOB directory.
'''

STEPSIZE = 150

def submit_subjobs():
    	cwd = os.getcwd()

    	# Modify this hard-coded path with your own preference
    	pyfile = '/home/friesner/tianchuan/cbeta_buildup/template/script_tools/jobDJ_scripts/run_plop_job.py'
    	host_list = [('foct', 120)]
    	job_dj = queue.JobDJ(verbosity="normal", hosts=host_list, max_failures=queue.NOLIMIT)
    	env_var_dict = {'PSP_CBETA_DATA':'/home/friesner/tianchuan/cbeta_data', 
		    	'PSP_RFS_LOGICALS':'/home/friesner/tianchuan/cbeta_data/rfs_logicals',
		    	'INTEL_LICENSE_FILE':'@fquad02:28518@fquad02', 
		    	'PSP_DATA':'/home/friesner/tianchuan/schrodinger_build/build/psp-v5.1/data/'}
    	for pattern in os.listdir(os.path.join(cwd, 'patterns')):
		print(pattern)
		os.chdir(os.path.join(cwd, 'patterns', pattern))
		newcwd = os.getcwd()
		for subjob in os.listdir(os.path.join(newcwd, 'subJobs')):
			if os.path.islink(os.path.join(newcwd, 'subJobs', subjob, '4KMT_localsamp.maegz')):
				iter_job_path = os.path.join(newcwd, 'subJobs', subjob)
				iterjob_confile_name = 'v92_' + subjob + '.con'
				iterjob_confile_path = os.path.join(iter_job_path, iterjob_confile_name)
				top_cmd = ['$SCHRODINGER/run', pyfile, iterjob_confile_path]
				job = queue.JobControlJob(top_cmd, command_dir=iter_job_path, launch_env_variables=env_var_dict)
				job_dj.addJob(job)
		os.chdir(cwd)	
	
	job_dj.run()
		
if __name__ == '__main__':
	submit_subjobs()
