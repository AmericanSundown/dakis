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
    p1.communicate()    # Wait till command is finished
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
        job_filename = join(JOBS_DIR, 'e%dt%d.sh' % (exp_id, resp_json.get('task_id') or resp_json.get('id')))
    return job_filename

def was_called_in_supercomputer():
    is_qsub_installed = subprocess.Popen('which qsub', stdout=subprocess.PIPE, shell=True)
    return bool(is_qsub_installed.communicate()[0])

def run_next_task(exp_id):
    '''Get task data, prepare executable, check if supercomputer, run_task.'''
    resp = requests.get('http://dakis.lt/api/exp/%d/next-task/' % exp_id)
    # logging.info('Getting next task: exp_id=%d, status_code=%d, resp=%s' % (exp_id, resp.status_code, resp.json()))
    print('Trying to run next task')
    if resp.status_code == 200 and resp.json():
        resp_json = resp.json()

        executable = prepare_executable(exp_id, resp_json['repository'], resp_json['branch'], resp_json['executable'])

        cmd = [
            '%s' % executable,       # Should pass path as it will be called  .strip('./')
            '--task_id=%s' % resp_json['task_id'],
            '--callback=%s' % join(MAIN_DIR, 'worker.py'),
        ]

        max_duration = 43200   # 12 hours
        for name, value in parse_json(resp_json['input_values']):
            name = ''.join(str(name).split())   # Note: this is protection for injection attack
            value = ''.join(str(value).split())
            cmd.append('--%s=%s' % (name, value))
            if name == 'max_duration' and int(value) > max_duration:
                max_duration = int(value)
        max_duration = '%d:%.2d:%.2d' % (max_duration / 3600, (max_duration % 3600) / 60, max_duration % 60)

        logging.info('Handling cmd: ' + ' '.join(cmd))

        try:
            if was_called_in_supercomputer():
                job_filename = get_job_filename(exp_id, resp_json)
                job_file = open(job_filename, 'w')
                job_file.write('#!/bin/bash\n#$ -j y\n#$ -l h_rt=%s\n#$ -S /bin/bash\n#$ -cwd\nmpirun -np 1 ' % max_duration)
                job_file.write(' '.join(cmd) + '\n')
                job_file.close()
                logging.info('Created job file: %s' % job_filename)
                add_to_queue_cmd = 'qsub -pe orte 1 -o {0}.o -e {0}.e {0}'.format(job_filename)
                # Note: should use separate files for stdout and stderr. Remove them only if they are empty or reported.
                p1 = subprocess.Popen(add_to_queue_cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , close_fds=True)
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
        name = name.lstrip('-')
        output_values.append([name, value])
    # logging.info('Sending: url=%s, data=%s' % (url, data))
    resp = requests.put(url, {'output_values': str(output_values), 'status': args.status})
    # logging.info('Response from sending: status_code=%s, data=%s' % (resp.status_code, resp.json()))
    return resp.json()


def prepare_executable(exp_id, repository, branch, exe_file):
    '''Clone and compile experiments code. Uses REST API if not all data provided in parameters.'''
    exe_dir = join(MAIN_DIR, 'exp_%d' % exp_id)
    executable = join(exe_dir, exe_file)

    # Note: commit head should also be saved to the task.
    if not os.path.exists(executable):  # Note: code version will be cached, new commits won't be pulled
        if not os.path.exists(exe_dir):
            if 'hg@' not in repository:
                cmd = 'git clone {0} {1} && cd {1} && git fetch origin {2} && git checkout {2} && git pull -r && make compile'.format(repository, exe_dir, branch)
            else:
                cmd = 'hg clone {0} {1} && cd {1} && make compile'.format(repository, exe_dir, branch)
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

    parser.add_argument('-task', '--task_id', type=int, help='Task ID', nargs=None, default=None)
    parser.add_argument('-st', '--status', type=str, help='Status of the task. D - done, S - suspended.', nargs=None, default='D')

    # Prepare environment arguments
    parser.add_argument('-env', '--prepare_environment', help='Create ~/.dakis dir and prepare environment', nargs='?', const=True)
    return parser


def main(args, unknown):
    global requests
    import requests

    if args.exp_id:
        run_next_task(args.exp_id)
    elif args.task_id:
        # Send results
        resp_json = send_task_results(args, unknown)
        # Remove job file if it exists
        exp_id = int(resp_json['experiment'].split('experiments')[-1].strip('/'))
        job_filename = get_job_filename(exp_id, resp_json)
        if os.path.isfile(job_filename):
            os.remove(job_filename)
        for file in os.listdir(JOBS_DIR):
            if file.endswith('.o') or file.endswith('.e'):  # Note: should split output and error streams
                os.remove(join(JOBS_DIR, file))
        ## Run next task
        if was_called_in_supercomputer():
            request_to_run_next_task(exp_id)   # Note: cannot start new job from inside of job
        else:
            run_next_task(exp_id)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.expanduser(join(MAIN_DIR, 'worker.log')),
        format='%(asctime)s - %(message)s',
    )
    logging.info('Called with argv: %s' % sys.argv)

    # Parse arguments
    args, unknown = get_argparser().parse_known_args()

    # Prepare environment
    if args.prepare_environment or not os.path.exists(MAIN_DIR) or not os.path.exists(JOBS_DIR):
        prepare_environment()

    # Get and run task
    main(args, unknown)
