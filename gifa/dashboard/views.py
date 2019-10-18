# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, json, urllib

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Q

from dashboard.models import Desa, Category, Refugee, Person
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

    # Marker icon resource from Map Box
    marker_url = "https://api.tiles.mapbox.com/v3/marker/pin-s-circle-stroked"

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
        "urlBaruPetaBIG": urlBaruPetaBIG
    }
    return render(request, 'dashboard/index.html', context)

def panel_disaster(request):

    # static dataset
    data = [
        {
            "first_name": "Cecep",
            "last_name": "Adi",
            "birth_date": "1970-04-03",
            "phone": "082213541291"
        },
        {
            "first_name": "Roby",
            "last_name": "Fauzi",
            "birth_date": "1986-06-23",
            "phone": "082213541291"
        },
        {
            "first_name": "Irsyad",
            "last_name": "Kharisma",
            "birth_date": "1987-01-01",
            "phone": "082213541331"
        },
        {

            "first_name": "Agung",
            "last_name": "Pratikno",
            "birth_date": "1966-04-03",
            "phone": "082213541291"
        },
    ]

    table = Refugee(data)
    # table = Refugee(Person.objects.all())
    return render(request, 'dashboard/disaster.html', {
        "table": table
        })

def panel_visualization(request):
    return render(request, 'dashboard/dataviz.html')
