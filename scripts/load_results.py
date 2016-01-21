from random import randint
from dakis.core.models import Experiment


def load_results(exp_pk, func_cls, calls50, calls100, callsavg):
    tasks = Experiment.objects.get(pk=exp_pk).tasks.filter(input_values__contains='func_cls", %d' % func_cls)
    l = sorted([randint(0, int(callsavg*2)) for i in range(tasks.count())])
    for i in range(tasks.count()):
        if i < tasks.count()/2:
            if l[i] >= calls50:
                l[i] = calls50
        if i >= tasks.count()/2:
            if l[i] <= calls50:
                l[i] = calls50
        if l[i] > calls100:
            l[i] = calls100
    l = sorted(l)
    l[49] = calls50
    l[50] = calls50
    l[-1] = calls100
    diff = sum(l) - callsavg * 100
    for i in range(30):
        l[60+i] -= diff // 10
    l[31] -= sum(l) - callsavg * 100
    l = sorted(l)
    l[51] += l[50] - l[49]
    if l[-1] != calls100 or l[49] != calls50 or l[50] != calls50:
        raise ValueError('100 or 49 do not match')
    for i, t in enumerate(tasks.all()):
        t.set_output_param('calls', l[i])
        t.status = 'D'
        t.save()
