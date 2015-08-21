import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dakis.core.models import Experiment


def index(request):
    return render(request, 'website/index.html', {
        'experiments': Experiment.objects.all(),
    })


def exp_details(request, exp_id):
    exp = Experiment.objects.get(pk=exp_id)
    unique_classes = exp.tasks.values_list('func_cls', flat=True).distinct()

    summaries = []
    for cls in unique_classes:
        tasks = exp.tasks.filter(func_cls=cls)
        tasks_count = tasks.count()
        calls = tasks.order_by('calls').values_list('calls', flat=True)
        subregions = tasks.values_list('subregions', flat=True)
        durations = tasks.values_list('duration', flat=True)
        total_duration = datetime.timedelta(0)
        for duration in durations:
            total_duration += duration
        summary = {
            'title': cls,
            'tasks_count': tasks_count,
            'calls_avg': sum(calls)/float(len(calls)),
            'calls_50': calls[int(tasks_count/2)],
            'calls_100': calls[len(calls)-1],
            'duration_avg': total_duration/float(len(durations)),
            'subregions_avg': sum(subregions)/float(len(durations)),
        }
        summaries.append(summary)

    return render(request, 'website/exp_details.html', {
        'exp': exp,
        'summaries': summaries,
    })
