from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dakis.core.models import Experiment


def index(request):
    return render(request, 'website/index.html', {
    })
