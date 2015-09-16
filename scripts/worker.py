#!/usr/bin/env python
import subprocess
import logging
import sys
import os
from os.path import join


MAIN_DIR = os.path.expanduser('~/.dakis')
JOBS_DIR = join(MAIN_DIR, 'jobs')


def prepare_environment():
    '''Prepares ~/.dakis directory and installs Python packages'''
    subprocess.Popen('mkdir -p %s && mv %s %s' % (JOBS_DIR, sys.argv[0], MAIN_DIR), shell=True)
    cmds = [
        'cd %s' % MAIN_DIR,
        'wget https://bootstrap.pypa.io/get-pip.py',
        'python get-pip.py --user',
        'rm get-pip.py',
        'pip install --user requests argparse || ~/.local/bin/pip install --user requests argparse',
    ]
    subprocess.Popen(' && '.join(cmds), shell=True)
    p1 = subprocess.Popen(' && '.join(cmds), shell=True)
    p1.communicate()  # TODO: replace with p1.wait()
    print("\n == Successfully prepared Dakis environment == \n")



def run_next_task(exp_id, executable, use_job=False):
    url = 'http://dakis.gimbutas.lt/api/exp/%d/next-task/' % exp_id
    resp = requests.get(url)
    task = resp.json()
    logging.info('Getting next task: exp_id=%d, status_code=%d, resp=%s' % (exp_id, resp.status_code, resp.json()))
    if resp.status_code == 200 and resp.json():
        cmd = [
            '%s' % executable,       # Should pass path as it will be called  .strip('./')
            '--gkls_cls=%s' % task['func_cls'],
            '--gkls_fid=%s' % task['func_id'],
            '--task_id=%s' % task['id'],
            '--callback=%s' % join(MAIN_DIR, 'worker.py'),
        ]
        try:
            if use_job:
                job_filename = join(JOBS_DIR, 'e%dc%df%d.sh' % (exp_id, task['func_cls'], task['func_id']))
                job_file = open(job_filename, 'w')
                job_file.write('#!/bin/bash\n#$ -j y\n#$ -S /bin/bash\n#$ -cwd\nmpirun -np 1 ')  # Header
                job_file.write(' '.join(cmd) + '\n')
                job_file.close()
                logging.info('Created job file: %s' % job_filename)
                add_to_queue_cmd = 'qsub -pe orte 1 -o {0}.o -e {0}.e {0}'.format(job_filename)
                # Specify stdout and stderr paths for qsub and remove them after execution
                print('Calling command:', add_to_queue_cmd)
                p1 = subprocess.Popen(add_to_queue_cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , close_fds=True)
                print('Add to queue command response:', p1.communicate())  # Error: cannot submit qsub job using ssh
                logging.info('Called command: %s' % add_to_queue_cmd)
            else:
                logging.info('Calling: cmd=%s' % ' '.join(cmd))
                subprocess.Popen(' '.join(cmd), shell=True, stdin=None, stdout=None, stderr=None)
        except Exception as e:
            logging.error('Got error while calling:  %s' % str(e))


def send_task_results(args):
    url = 'http://dakis.gimbutas.lt/api/tasks/%d/' % args.task_id
    data = {
        'calls': args.calls,
        'duration': args.duration,
        'subregions': args.subregions,
        'status': args.status,
    }
    logging.info('Sending: url=%s, data=%s' % (url, data))
    resp = requests.put(url, data)
    logging.info('Response from sending: status_code=%s, data=%s' % (resp.status_code, resp.json()))
    return resp.json()


def prepare_executable(args):
    '''Clone and compile experiments code. Uses REST API if not all data provided in parameters.'''
    exp_id = args.exp_id
    if args.repository and args.branch and args.executable:
        repository = args.repository
        branch = args.branch
        exe_file = args.executable
    else:
        url = 'http://dakis.gimbutas.lt/api/experiments/%d/' % exp_id
        resp = requests.get(url)
        exp = resp.json()
        repository = exp['repository']
        branch = exp['branch']
        exe_file = exp['executable']

    exe_dir = join(MAIN_DIR, 'exp_%d' % exp_id)
    executable = join(exe_dir, exe_file)

    if not os.path.exists(executable):  # Note: code version will be cached, new commits won't be pulled
        if not os.path.exists(exe_dir):
            cmd = 'git clone {0} {1} && cd {1} && git fetch origin {2} && git checkout {2} && git pull -r && make'.format(repository, exe_dir, branch)
            subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        else:
            subprocess.Popen('cd %s && git pull -r && make' % exe_dir, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    return executable


def request_to_run_next_task(exp_id):
    url = 'http://dakis.gimbutas.lt/api/exp/%d/run/' % exp_id
    resp = requests.get(url)
    return


def get_argparser():
    import argparse
    parser = argparse.ArgumentParser(description='Schedules tasks')
    parser.add_argument('-exp', '--exp_id', type=int, help='Experiment ID', nargs='?', default=None)
    parser.add_argument('-exe', '--executable', type=str, help='Executable file', nargs='?', default=None)
    parser.add_argument('-rep', '--repository', type=str, help='Source code repository', nargs='?', default=None)
    parser.add_argument('-br', '--branch', type=str, help='Repository branch', nargs='?', default=None)

    # Worker should find the job by itself.
    parser.add_argument('-j', '--job', help='Create job and execute task through supercomputer task queue', nargs='?', const=True)

    parser.add_argument('-task', '--task_id', type=int, help='Task ID', nargs=None, default=None)
    parser.add_argument('-calls', '--calls', type=int, help='Number of calls', nargs=None, default=None)
    parser.add_argument('-duration', '--duration', type=float, help='Execution duration', nargs=None, default=None)
    parser.add_argument('-subs', '--subregions', type=int, help='Number of subregions', nargs=None, default=None)
    parser.add_argument('-st', '--status', type=str, help='Status of the task. D - done, S - suspended.', nargs=None, default=None)

    # Prepare environment arguments
    parser.add_argument('-env', '--prepare_environment', help='Create ~/.dakis dir and prepare environment', nargs='?', const=True)
    return parser


def main():
    global requests
    import requests
    args = get_argparser().parse_args()

    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.expanduser(join(MAIN_DIR, 'worker.log')),
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info('Invoked with argv: %s' % sys.argv)
    logging.info('Invoked with: exp_id=%s executable=%s task_id=%s calls=%s -duration=%s --subregions=%s --status=%s --job=%s' % (
                 args.exp_id, args.executable, args.task_id, args.calls, args.duration, args.subregions, args.status, args.job))

    if args.exp_id:
        exe = prepare_executable(args)
        run_next_task(args.exp_id, exe, args.job)
    elif args.task_id:
        # Send results
        resp_json = send_task_results(args)
        # Remove job file if it exists
        exp_id = int(resp_json['experiment'].split('experiments')[-1].strip('/'))
        job_filename = join(JOBS_DIR, 'e%dc%df%d.sh' % (exp_id, resp_json['func_cls'], resp_json['func_id']))
        if os.path.isfile(job_filename):
            os.remove(job_filename)
        for file in os.listdir(JOBS_DIR):
            if file.endswith('.o') or file.endswith('.e'):
                os.remove(join(JOBS_DIR, file))
        request_to_run_next_task(exp_id)


if __name__ == '__main__':
    if (not os.path.exists(MAIN_DIR) or not os.path.exists(JOBS_DIR)
        or 'env' in sys.argv or '-env' in sys.argv or '--prepare_environment' in sys.argv):
        prepare_environment()
    else:
        main()
