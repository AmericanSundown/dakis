#!/usr/bin/env python3
import argparse
import requests
import sys
import subprocess
import datetime
import pytimeparse


def timedelta_format(string):
    return datetime.timedelta(seconds=pytimeparse.timeparse.timeparse(string))

parser = argparse.ArgumentParser(description='Schedules tasks')
parser.add_argument('-exp', '--exp_id', type=int, help='Experiment ID', nargs='?', default=None)
parser.add_argument('-exe', '--executable', type=str, help='Executable file', nargs='?', default=None)

parser.add_argument('-task', '--task_id', type=int, help='Task ID', nargs=None, default=None)
parser.add_argument('-calls', '--calls', type=int, help='Number of calls', nargs=None, default=None)
parser.add_argument('-duration', '--duration', type=timedelta_format, help='Execution duration', nargs=None, default=None)
parser.add_argument('-subs', '--subregions', type=int, help='Number of subregions', nargs=None, default=None)
parser.add_argument('-st', '--status', type=int, help='Status of the task. D - done, S - suspended.', nargs=None, default=None)


def run_next_task(exp_id, executable):
    url = 'http://dakis.gimbutas.lt/api/%d/next_task/' % exp_id
    resp = requests.get(url)
    task = resp.json()
    if resp.status_code == 200 and resp.json():
        subprocess.Popen([
            './%s' % executable,
            '-cls=%d' % task['func_cls'],
            '-fid=%d' % task['func_id'],
            '-id=%d' % task['id'],
            '--callback=%s' % sys.argv[0],
        ],
        stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)


def send_task_results(args):
    url = 'http://dakis.gimbutas.lt/api/tasks/%d/' % args.task_id
    data = {
        'calls': args.calls,
        'duration': args.duration,
        'subregions': args.subregions,
        'status': args.status,
    }
    resp = requests.put(url, data)
    exp_id = resp.json()['experiment'].split('experiments')[-1].strip('/')
    return int(exp_id)


def main(args):
    if args.exp_id:
        if not args.executable:
            raise ValueError('Provide executable file (-exe=) for this experiment')
        run_next_task(args.exp_id, args.executable)
    elif args.task_id:
        exp_id = send_task_results(args)
        run_next_task(exp_id, args.executable)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
