# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, urllib

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q

from dashboard.models import Desa
from odkcollect.models import ODKConnector

def gifa_dashboard(request):
    """
    GIFA Dashboard
    """
    # Desa Boundary
    desa_bndy = Desa.objects.filter(Q(nama='BALEENDAH') | Q(nama='ANDIR'))
    desa_bndy_json = serialize(
        'geojson',
        desa_bndy,
        geometry_field='polygon',
        fields=('nama', 'luas', 'catatan')
    )

    # ODK Polyline
    all_odk_polyline = ODKConnector.objects.filter(publish=True)

    context = {
        "desa_bndy_json": desa_bndy_json,
        "all_odk_polyline": all_odk_polyline
    }
    return render(request, 'dashboard/index.html', context)
