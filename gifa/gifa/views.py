from django.shortcuts import render
from django.conf import settings

from odkcollect.models import ODKConnector

def page_home(request):
    """
    Ini kyk semacam controller
    """
    name = "Rizky"
    data = ODKConnector.objects.filter(publish=True) # ini contoh ORM data dari tabel odkcollector_odkconnector
    context = {
        "name": name,
        "data": data
    }
    return render(request, 'gifa/page_home.html', context)
