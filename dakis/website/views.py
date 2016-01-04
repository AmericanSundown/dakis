import datetime
import json
import logging
import subprocess
import collections

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.models import Site

from dakis.core.models import Experiment, Task
from dakis.website.forms import PropertyForm

logger = logging.getLogger(__name__)


def index(request):
    exps = Experiment.objects.filter(is_major=True).order_by('-created')
    if request.user.is_authenticated():
        exps = exps.filter(author=request.user)
    return render(request, 'website/index.html', {
        'experiments': exps,
    })


def toggle_exp_status(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    if (exp.tasks.filter(status='C') | exp.tasks.filter(status='R')).exists():
        if exp.status != 'R':
            exp.status = 'R'
            if not request.user.profile.hostname or not request.user.profile.host_password:
                messages.error(request, ugettext('Hostname or host password not set in UserProfile'))
            else:
                run_worker(exp, request.user)
                if not exp.threads:
                    exp.threads = 1
                else:
                    exp.threads += 1
                # messages.success(request, ugettext('New thread was started successfully'))
        else:
            exp.status = 'P'
            exp.threads = 0
        exp.save()
    elif exp.tasks.filter(status='D').exists():
        exp.status = 'D'
        exp.threads = 0
        exp.save()
    else:
        if not exp.tasks.all():
            exp.create_tasks()
        exp.status = 'R'
        exp.threads += 1
        exp.save()
        run_worker(exp, request.user)
    return redirect(exp)


def add_exp_property(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            exp.details.append((form.cleaned_data['name'], form.cleaned_data['value']))
            exp.save()
    return redirect(exp)


def remove_exp_property(request, exp_id, prop_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    exp.details.pop(int(prop_id))
    exp.save()
    return redirect(exp)


def run_worker(exp, user):
    cmd = 'sshpass -p%s ssh -o "StrictHostKeyChecking no" %s ' \
          '"source /etc/profile; .dakis/worker.py -exp=%d"' % (
        user.profile.host_password,
        user.profile.hostname,
        exp.pk,
    )
    logger.info('Running: ' + cmd)

    subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    exp.save()   # Note: Why exp is saved here?
    return


def run_worker_view(request, exp_id):
    logger.debug('Requested to run exp with id=' + str(exp_id))
    exp = get_object_or_404(Experiment, pk=exp_id)
    user = exp.author
    if not user.profile.hostname or not user.profile.host_password:
        messages.error(request, ugettext('Hostname or host password not set in UserProfile'))
    else:
        run_worker(exp, user)
    return redirect(exp)


def start_worker_view(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    user = exp.author
    if not user.profile.hostname or not user.profile.host_password:
        messages.error(request, ugettext('Hostname or host password not set in UserProfile'))
    else:
        if not exp.threads:
            exp.threads = 1
        else:
            exp.threads += 1
        exp.save()
        run_worker(exp, user)
    return redirect(exp)


def get_next_task(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    domain = Site.objects.get_current().domain
    if exp.tasks.filter(status='C').exists() and exp.status in 'CR':
        task = exp.tasks.filter(status='C').first()
        task.status = 'R'
        task.save()
        return HttpResponse(json.dumps({
            'experiment': 'http://' + domain + reverse('experiment-detail', args=[exp.pk]),
            'input_values': task.input_values,
            'task_id': task.pk,
            'repository': task.experiment.algorithm.repository,
            'branch': task.experiment.algorithm.branch,
            'executable': task.experiment.algorithm.executable,
        }), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")


def create_gkls_tasks(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    if exp.tasks.all().count() < 800:
        for cls in range(1, 9):
            for fid in range(1, 101):
                Task.objects.create(experiment=exp, func_cls=cls, func_id=fid)
    return redirect(exp)


def operate(param_name, tasks, operator):
    vals = []
    for task in tasks:
        for name, value in task.output_values:
            if name == param_name:
                vals.append(value)
    vals = sorted(vals)
    if operator == 'avg' or operator == 'average' or operator == 'mean':
        return sum(vals) / len(vals)
    elif operator == 'median':
        if len(vals) % 2 == 1:
            return vals[len(vals) // 2]
        return (vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2
    elif operator == 'max':
        return max(vals)
    elif operator == 'min':
        return min(vals)


def exp_details(request, exp_id):
    '''Generates table(s) for single algorithm results. Each table contains:
    Table header
    Table row with values for each group value'''
    exp = get_object_or_404(Experiment, pk=exp_id)

    tables = []

    # Find display parameter groups: {key: [col, param, operator], ..}
    display_param_groups = collections.OrderedDict()
    for p in exp.problem.result_display_params:
        col_name = p.get('column_name')
        param_name = p.get('parameter_name')
        operator = p.get('operator')
        group_name = p.get('group_by')
        if group_name not in display_param_groups.keys():
            display_param_groups[group_name] = [[col_name, param_name, operator]]
        else:
            display_param_groups[group_name].append([col_name, param_name, operator])

    # Handle each group
    for group_key in display_param_groups.keys():
        table = []    # Structure: [[col_name, col_name, ..], [val, val, ..], [val, val, ..], ..]

        param_list = display_param_groups[group_key]    # [[col, param, op], ..]

        # Get table header
        table_header = [group_key, 'Done', 'Suspended']
        for col_name, param_name, operator in param_list:
            table_header.append(col_name)
        table.append(table_header)

        # Handle each param in this group
        unique_values = exp.get_unique_task_input_param_values(group_key)   # Note: how to handle empty group key?
        for value in unique_values:
            if type(value) == str or type(value) == unicode:
                tasks = exp.tasks.filter(input_values__contains='["%s", "%s"]' % (group_key, value))
            else:
                tasks = exp.tasks.filter(input_values__contains='["%s", %s]' % (group_key, value))

            table_row = [value, tasks.filter(status='D').count(), tasks.filter(status='S').count()]

            for col_name, param_name, op_name in table_row:
                result = operate(param_name, tasks, op_name)
                table_row.append(result)
            table.append(table_row)
        tables.append(table)

    return render(request, 'website/exp_details.html', {
        'exp': exp,
        'tables': tables,
    })


def fork_exp(request, exp_id):
    exp = get_object_or_404(Experiment, pk=exp_id)
    # Creates new Experiment instance and copies all its fields.
    new_exp = exp.dublicate()
    return redirect(new_exp)


def reset_exp_tasks(request, exp_id, task_status):
    exp = get_object_or_404(Experiment, pk=exp_id)
    for task in exp.tasks.all():
        if task.status == task_status:
            task.status = 'C'
            task.save()
    return redirect(exp)


def reset_cls_tasks(request, exp_id, func_cls, task_status):
    '''Resets all suspended tasks in same class as provided task'''
    exp = get_object_or_404(Experiment, pk=exp_id)
    for task in exp.tasks.filter(func_cls=func_cls):
        if task.status == task_status:
            task.status = 'C'
            task.save()
    return redirect(exp)


def compare_exps(request):
    '''Generates tables for algorithm comparison
    Table title
    Table block - group value
        Table row - algorithm'''
    exp_pks = request.GET.get('exps', '').split(',')
    exps = []
    unique_classes = set()
    for exp_pk in exp_pks:
        exp = get_object_or_404(Experiment, pk=exp_pk)
        exps.append(exp)

        for cls in exp.tasks.values_list('func_cls', flat=True).order_by('func_cls').distinct():
            unique_classes.add(cls)

    # list detail exp
    summaries = []
    for cls in unique_classes:
        summary = {
            'algorithm': [],
            'exp_pk': [],
            'cls': [],
            'title': [],     # How to mark, which is the highest? Should I pack color too? - simples solution.
            'tasks_count': [],
            'tasks_suspended': [],
            'calls_avg': [],
            'calls_50': [],
            'calls_100': [],
            'duration_avg': [],
            'subregions_avg': [],
        }

        for exp in exps:
            tasks_done = exp.tasks.filter(func_cls=cls, status="D")
            tasks_suspended = exp.tasks.filter(func_cls=cls, status="S")
            tasks = tasks_done | tasks_suspended
            if tasks.exists():
                calls = tasks.order_by('calls').values_list('calls', flat=True)
                subregions = tasks.values_list('subregions', flat=True)
                durations = tasks.values_list('duration', flat=True)
                summary['algorithm'].append(exp.algorithm)
                summary['exp_pk'].append(exp.pk)
                summary['cls'].append(cls)
                summary['tasks_count'].append(tasks_done.count())
                summary['tasks_suspended'].append(tasks_suspended.count())
                summary['calls_avg'].append(sum([c for c in calls if c])/float(len(calls)))
                summary['calls_100'].append(calls[len(calls)-1])
                summary['duration_avg'].append(sum([d for d in durations if d])/float(len(durations)))
                summary['subregions_avg'].append(sum([s for s in subregions if s])/float(len(subregions)))
                if len(calls) % 2 == 1:
                    summary['calls_50'].append(calls[len(calls)//2])
                else:
                    summary['calls_50'].append((calls[len(calls)//2-1] + calls[len(calls)//2])/2)
        summaries.append(summary)

    return render(request, 'website/exps_comparison.html', {
        'exps': exps,
        'summaries': summaries,
    })
