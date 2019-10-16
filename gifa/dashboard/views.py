# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, urllib

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q

from dashboard.models import Desa, Category
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
    all_odk_polyline = ODKConnector.objects.filter(
        publish=True,
        geometry_type='polyline'
    )

    # ODK Polygon
    all_odk_polygon = ODKConnector.objects.filter(
        publish=True,
        geometry_type='polygon'
    )

    # ODK Point
    all_odk_point = ODKConnector.objects.filter(
        publish=True,
        geometry_type='point'
    )

    # category
    all_category = Category.objects.all()

    context = {
        "desa_bndy_json": desa_bndy_json,
        "all_odk_polyline": all_odk_polyline,
        "all_odk_polygon": all_odk_polygon,
        "all_odk_point": all_odk_point,
        "all_category": all_category
    }
    return render(request, 'dashboard/index.html', context)
