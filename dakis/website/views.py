import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dakis.core.models import Experiment, Task


def index(request):
    return render(request, 'website/index.html', {
        'experiments': Experiment.objects.all(),
    })


def create_gkls_tasks(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    if exp.tasks.all().count() < 800:
        for cls in range(1, 9):
            for fid in range(1, 101):
                Task.objects.create(experiment=exp, func_cls=cls, func_id=fid)
    return redirect(exp)


def exp_details(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    unique_classes = exp.tasks.values_list('func_cls', flat=True).distinct()

    summaries = []
    for cls in unique_classes:
        tasks = exp.tasks.filter(func_cls=cls, status="D")
        tasks_count = tasks.count()
        if tasks_count:
            calls = tasks.order_by('calls').values_list('calls', flat=True)
            subregions = tasks.values_list('subregions', flat=True)
            durations = tasks.values_list('duration', flat=True)
            total_duration = datetime.timedelta(0)
            for duration in durations:
                if duration:
                    total_duration += duration
            summary = {
                'title': cls,
                'tasks_count': tasks_count,
                'calls_avg': sum([c for c in calls if c])/float(len(calls)),
                'calls_50': calls[int(tasks_count/2)],
                'calls_100': calls[len(calls)-1],
                'duration_avg': total_duration/float(len(durations)),
                'subregions_avg': sum([s for s in subregions if s])/float(len(durations)),
            }
            summaries.append(summary)

    return render(request, 'website/exp_details.html', {
        'exp': exp,
        'summaries': summaries,
    })
