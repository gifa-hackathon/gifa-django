# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json

from django.http import JsonResponse

from odkcollect.help import odk_to_json
from odkcollect.models import ODKConnector

def get_odk_geojson(request, con_id):
    """
    Get GeoJson for ODK Collect
    """
    try:
        odk_con = ODKConnector.objects.get(con_id=con_id)
        routegsjon = odk_to_json(odk_con)
        return JsonResponse(routegsjon)
    except Exception as err:
        return JsonResponse({'error': str(err)})
