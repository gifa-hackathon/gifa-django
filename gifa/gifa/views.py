from django.shortcuts import render
from django.conf import settings

from odkcollect.models import ODKConnector

def page_home(request):
    """
    Page Home
    """
    context = {}
    return render(request, 'gifa/page_home.html', context)
