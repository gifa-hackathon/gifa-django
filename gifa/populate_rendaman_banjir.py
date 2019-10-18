import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import RendamanBanjir

shp_file = 'datashp/Rendaman_Banjir/Rendaman_Banjir.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id' : 'Id',
    'luas': 'Luas',
    'polygon': 'Polygon'
} # The mapping is a dictionary

lm = LayerMapping(RendamanBanjir, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
