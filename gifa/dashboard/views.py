# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, urllib

from django.shortcuts import render
from django.utils.safestring import mark_safe

def gifa_dashboard(request):
    """
    GIFA Dashboard
    """

    context = {}
    return render(request, 'dashboard/index.html', context)
