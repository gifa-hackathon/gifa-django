import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import BangunanOSM

shp_file = 'datashp/bangunan_osm/bangunan_osm.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id' : 'osm_way_id',
    'nama': 'name',
    'jenis_bangunan': 'building',
    'polygon': 'Polygon'
} # The mapping is a dictionary

lm = LayerMapping(BangunanOSM, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
