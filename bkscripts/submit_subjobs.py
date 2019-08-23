# Ben's modified version of submission script for pre-generated confiles with
# ranges of seeds and iteration numbers.

# Proper way to call this script:
# enhanced_subjob_submission analysis 3 SEEDRANGE ITERRANGE

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

def submit_subjobs(job_type, job_mode, seed_start, seed_end, iter_start, iter_end):
    cwd = os.getcwd()
    # Modify this hard-coded path with your own preference
    pyfile = '/home/friesner/tianchuan/cbeta_buildup/template/script_tools/jobDJ_scripts/run_plop_job.py'
    host_list = [('foct', 30)]
    job_dj = queue.JobDJ(verbosity="normal", hosts=host_list, max_failures=queue.NOLIMIT)
    env_var_dict = {'PSP_CBETA_DATA':'/home/friesner/tianchuan/cbeta_data', 
                    'PSP_RFS_LOGICALS':'/home/friesner/tianchuan/cbeta_data/rfs_logicals',
                    'INTEL_LICENSE_FILE':'@fquad02:28518@fquad02', 
                    'PSP_DATA':'/home/friesner/tianchuan/schrodinger_build/build/psp-v5.1/data/'}
	# modified by bk	
    if job_type == 'analysis':
	if job_mode == 0:
		for seed in range(seed_start, seed_end + 1):
		    for iter in range(iter_start, iter_end + STEPSIZE, STEPSIZE):
			iter_job_path = os.path.join(cwd, 'subJobs', str(seed) + '_' + str(iter))
			iterjob_confile_name = 'v92_' + str(seed) + '_' + str(iter) + '.con'
			iterjob_confile_path = os.path.join(iter_job_path, iterjob_confile_name)
			top_cmd = ['$SCHRODINGER/run', pyfile, iterjob_confile_path]
			job = queue.JobControlJob(top_cmd, command_dir=iter_job_path, launch_env_variables=env_var_dict)
			job_dj.addJob(job)
	if job_mode == 1:
		for dirname in reversed(os.listdir(os.path.join(cwd, 'subJobs'))):
			iter_job_path = os.path.join(cwd, 'subJobs', dirname)
			iterjob_confile_name = 'v92_' + dirname + '.con'
			iterjob_confile_path = os.path.join(iter_job_path, iterjob_confile_name)
			top_cmd = ['$SCHRODINGER/run', pyfile, iterjob_confile_path]
			job = queue.JobControlJob(top_cmd, command_dir=iter_job_path, launch_env_variables=env_var_dict)
			job_dj.addJob(job)
			
    job_dj.run()
		

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('job_type',
                        type=str,
                        help='main: submit normal subjobs;\
                              iter100:submit iter100 jobs.')
    parser.add_argument('job_mode', 
                        type=int,
                        help='1: Run everything including subjob folder generation;\
                              2: Just submit subjobs.\
                              3. Resubmit those subjobs died accidentally.')
    parser.add_argument('seed_start',
			type=int, default=1,
			help='min seed')
    parser.add_argument('seed_end',
			type=int, default=1,
			help='max seed')
    parser.add_argument('iter_start',
			type=int, default=1,
			help='min iteration number')
    parser.add_argument('iter_end',
			type=int, default=1,
			help='max iteration number')
    args = parser.parse_args()

    cwd = os.getcwd()

    if args.job_type == 'analysis':
	    submit_subjobs(args.job_type, args.job_mode, args.seed_start, args.seed_end, args.iter_start, args.iter_end)
