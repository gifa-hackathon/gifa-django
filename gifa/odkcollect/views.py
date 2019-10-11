# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json

from django.http import JsonResponse

from odkcollect.help import odk_to_json

def get_odk_geojson(request):
    """
    Get GeoJson for ODK Collect
    """
    routegsjon = odk_to_json()
    return JsonResponse(routegsjon)
