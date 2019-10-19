import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import InfrastrukturJalanOSM

shp_file = 'datashp/infrastruktur_jalan_osm/infrastrutur_jalan_osm.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id': 'osm_id',
    'nama' : 'name',
    'jenis_jalan' : 'highway',
    'keterangan' : 'other_tags',
    'polyline': 'LineString'
} # The mapping is a dictionary

lm = LayerMapping(InfrastrukturJalanOSM, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
