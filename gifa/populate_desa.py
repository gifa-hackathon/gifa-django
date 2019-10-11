import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import Desa

shp_file = 'datashp/Admin_Desa_BPS2015_Baleendah.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id' : 'OBJECTID',
    'nama' : 'DESA',
    'luas': 'Shape_Area',
    'polygon': 'Polygon'
} # The mapping is a dictionary

lm = LayerMapping(Desa, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
