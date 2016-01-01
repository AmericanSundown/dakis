#!/usr/bin/env python
import subprocess
import logging
import sys
import os
import json
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


def parse_json(value):
    if type(value) == str or type(value) == unicode:
        return json.loads(value.replace("'", '"'))
    return value

def get_job_filename(exp_id, resp_json):
    input_values = dict(parse_json(resp_json['input_values']))
    if input_values.get('func_cls') and input_values.get('func_id'):
        job_filename = join(JOBS_DIR, 'e%dc%df%d.sh' % (exp_id, input_values['func_cls'], input_values['func_id']))
    else:
        job_filename = join(JOBS_DIR, 'e%t%d.sh' % (exp_id, resp_json['task_id']))
    return job_filename


def run_next_task(exp_id, executable=None, use_job=False):
    url = 'http://dakis.lt/api/exp/%d/next-task/' % exp_id
    resp = requests.get(url)
    logging.info('Getting next task: exp_id=%d, status_code=%d, resp=%s' % (exp_id, resp.status_code, resp.json()))
    if resp.status_code == 200 and resp.json():
        resp_json = resp.json()
        cmd = [
            '%s' % executable,       # Should pass path as it will be called  .strip('./')
            '--task_id=%s' % resp_json['task_id'],
            '--callback=%s' % join(MAIN_DIR, 'worker.py'),
        ]
        for name, value in parse_json(resp_json['input_values']):
            name = ''.join(str(name).split())   # Note: this is protection for injection attack
            value = ''.join(str(value).split())
            cmd.append('--%s=%s' % (name, value))

        logging.info('Handling cmd: ' + ' '.join(cmd))

        try:
            if use_job:
                job_filename = get_job_filename(exp_id, resp_json)
                job_file = open(job_filename, 'w')
                job_file.write('#!/bin/bash\n#$ -j y\n#$ -l h_rt=12:00:00\n#$ -S /bin/bash\n#$ -cwd\nmpirun -np 1 ')  # Header
                job_file.write(' '.join(cmd) + '\n')
                job_file.close()
                logging.info('Created job file: %s' % job_filename)
                add_to_queue_cmd = 'qsub -pe orte 1 -o {0}.o -e {0}.e {0}'.format(job_filename)
                # Note: should use separate files for stdout and stderr. Remove them only if they are empty or reported.
                p1 = subprocess.Popen(add_to_queue_cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , close_fds=True)
                # Note: should parse qsub job id:  p1.communicate()
                logging.info('Called command: %s' % add_to_queue_cmd)
            else:
                # logging.info('Calling: cmd=%s' % ' '.join(cmd))
                subprocess.Popen(' '.join(cmd), shell=True, stdin=None, stdout=None, stderr=None)
        except Exception as e:
            logging.error('Got error while calling:  %s' % str(e))


def send_task_results(args, unknown):
    url = 'http://dakis.lt/api/tasks/%d/' % args.task_id
    output_values = []
    for p in unknown:
        name, value = p.split('=')
        name.strip('-')
        output_values.append([name, value])
    # logging.info('Sending: url=%s, data=%s' % (url, data))
    resp = requests.put(url, {'output_values': str(output_values), 'status': args.status})
    # logging.info('Response from sending: status_code=%s, data=%s' % (resp.status_code, resp.json()))
    return resp.json()


def prepare_executable(args):
    '''Clone and compile experiments code. Uses REST API if not all data provided in parameters.'''
    exp_id = args.exp_id
    if args.repository and args.branch and args.executable:
        repository = args.repository
        branch = args.branch
        exe_file = args.executable
    else:
        url = 'http://dakis.lt/api/experiments/%d/' % exp_id
        resp = requests.get(url)
        exp = resp.json()
        repository = exp['repository']    # Note: This information should be provided through Task API (during exp_pk request)
        branch = exp['branch']            # API URL should be implemented using view, not django-rest-framework
        exe_file = exp['executable']      # URL is: http://dakis.lt/api/exp/%d/next-task/'

    exe_dir = join(MAIN_DIR, 'exp_%d' % exp_id)
    executable = join(exe_dir, exe_file)

    if not os.path.exists(executable):  # Note: code version will be cached, new commits won't be pulled
        if not os.path.exists(exe_dir):
            cmd = 'git clone {0} {1} && cd {1} && git fetch origin {2} && git checkout {2} && git pull -r && make compile'.format(repository, exe_dir, branch)
            proc = subprocess.Popen(cmd, shell=True)
            proc.communicate()
        else:
            proc = subprocess.Popen('cd %s && git pull -r && make compile' % exe_dir, shell=True)  # Use ``make compile`` instead of ``make``
            proc.communicate()
    return executable


def request_to_run_next_task(exp_id):
    url = 'http://dakis.lt/api/exp/%d/run/' % exp_id
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
    parser.add_argument('-st', '--status', type=str, help='Status of the task. D - done, S - suspended.', nargs=None, default=None)

    # Prepare environment arguments
    parser.add_argument('-env', '--prepare_environment', help='Create ~/.dakis dir and prepare environment', nargs='?', const=True)
    return parser


def main():
    global requests
    import requests
    args, unknown = get_argparser().parse_known_args()

    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.expanduser(join(MAIN_DIR, 'worker.log')),
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info('Called with argv: %s' % sys.argv)
    # logging.info('Invoked with: exp_id=%s executable=%s task_id=%s calls=%s -duration=%s --subregions=%s --status=%s --job=%s' % (
    #              args.exp_id, args.executable, args.task_id, args.calls, args.duration, args.subregions, args.status, args.job))

    if args.exp_id:
        exe = prepare_executable(args)
        run_next_task(args.exp_id, exe, args.job)
    elif args.task_id:
        # Send results
        resp_json = send_task_results(args, unknown)
        print('Sent results, got response: ' + str(resp_json))
        # Remove job file if it exists
        exp_id = int(resp_json['experiment'].split('experiments')[-1].strip('/'))
        job_filename = get_job_filename(exp_id, resp_json)
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
    main()
