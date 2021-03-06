# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, urllib, json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.db import connection

from dashboard.models import Desa, Category, BangunanOSM
from odkcollect.models import ODKConnector
from mapservice.models import MapServices, LayerServices

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

    # Marker icon resource from Map Box
    marker_url = "https://api.tiles.mapbox.com/v3/marker/pin-s-circle-stroked"

    # WMS Services
    all_map_services = MapServices.objects.filter(
        publish=True
    )

    # BIG Basemap Services
    urlPetaBIG = "https://portal.ina-sdi.or.id/arcgis/rest/services/IGD/RupabumiIndonesia/MapServer"
    urlBaruPetaBIG = "http://palapa.big.go.id:8080/geoserver/gwc/service/tms/1.0.0/basemap_rbi:basemap@EPSG:3857@png/{z}/{x}/{-y}.png"

    # category
    all_category = Category.objects.all()

    context = {
        "desa_bndy_json": desa_bndy_json,
        "all_odk_polyline": all_odk_polyline,
        "all_odk_polygon": all_odk_polygon,
        "all_odk_point": all_odk_point,
        "all_category": all_category,
        "marker_url": marker_url,
        "urlPetaBIG": urlPetaBIG,
        "urlBaruPetaBIG": urlBaruPetaBIG,
        "all_map_services": all_map_services
    }

    return render(request, 'dashboard/index.html', context)

def panel_affected_family(request):
    return render(request, 'dashboard/affected_family.html')

def panel_humanitarian_aid(request):
    return render(request, 'dashboard/humanitarian_aid.html')

def panel_visualization(request):
    return render(request, 'dashboard/dataviz.html')

def panel_vulnerability(request):
    return render(request, 'dashboard/vulnerability.html')

def panel_exposure(request):
    return render(request, 'dashboard/exposure.html')

def panel_bangunanosm(request):
    # Getting data from database
    bangunan_osm = BangunanOSM.objects.values('id', 'nama', 'jenis_bangunan', 'exposure_index', 'flood_depth')
    bangunan_osm_json = json.dumps({"data": list(bangunan_osm)})
    data = {'bangunan_osm': bangunan_osm_json, }
    return HttpResponse(bangunan_osm_json, content_type="application/json")