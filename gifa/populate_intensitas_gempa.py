import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import IntensitasGempa

shp_file = 'datashp/intensitasgempa_mi/intensitasgempa_mi.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id' : 'PGAPOL_ID',
    'luas': 'AREA',
    'polygon': 'Polygon',
    'value': 'VALUE'
} # The mapping is a dictionary

lm = LayerMapping(IntensitasGempa, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
