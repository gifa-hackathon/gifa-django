import psycopg2
import psycopg2.extras

from django.conf import settings
from django.contrib.gis.geos import Point, Polygon

from geojson import (
    MultiLineString,
    Polygon as PolygonJson,
    Point as PointJson,
    Feature,
    FeatureCollection
)

from dashboard.models import (
    IntensitasGempa,
    RendamanBanjir,
    SesarLembang
)

def inspect_earthquake_intensity(odkgeom, properties_dict):
    """
    Inspect ODK object based on earthquake intensity data
    """
    intersaction_list = IntensitasGempa.objects.filter(polygon__intersects=odkgeom)
    if intersaction_list:
        stmpart1 = "Berdasarkan data intensitas gempa, lokasi,"
        stmpart2 = "ini berada pada wilayah dengan magnitudo"
        unit = "SR"
        stmpart3 = "atau skala"
        mmi = "<a href='https://www.bmkg.go.id/gempabumi/skala-mmi.bmkg' target='_blank'>I</a>"
        info_statement = "%s <strong>%s</strong> %s <strong>%s %s</strong>, %s %s" % (
            stmpart1,
            next(iter(properties_dict.values())),
            stmpart2,
            intersaction_list[0].value,
            unit,
            stmpart3,
            mmi
        )
    else:
        info_statement = "<p>Lokasi ini diluar data intensitas gempa</p>"
    return info_statement


def read_odk_image(odk_con, properties_dict, record, colnames):
    """
    Read ODK Image and put inside properties
    """
    if odk_con.geometry_type == 'polygon':
        image_columns = [i.strip() for i in odk_con.geoshape_image.split(";")]
    elif odk_con.geometry_type == 'polyline':
        image_columns = [i.strip() for i in odk_con.geotrace_image.split(";")]
    elif odk_con.geometry_type == 'point':
        image_columns = [i.strip() for i in odk_con.geopoint_image.split(";")]

    for image in image_columns:
        odk_agrgt_url = '%s%s%s%s%s%s%s%s%s' % (
            settings.ODK_AGGREGATE_HOST,
            'view/binaryData?blobKey=',
            odk_con.odk_table_name,
            '%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2F',
            odk_con.odk_table_name,
            '%5B%40key%3D',
            record[colnames.index("META_INSTANCE_ID")].replace(":","%3A"),
            '%5D%2F',
            image
        )
        properties_dict.update({image.upper():"<img src=\'%s\' height='350' width='350'>" % odk_agrgt_url})


def odk_to_json(odk_con):
    """
    Convert ODK to JSON
    """
    try:
        # Connect Databases
        connection = psycopg2.connect(
            user = odk_con.db_username,
            password = odk_con.db_password,
            host = odk_con.db_host,
            port = odk_con.db_port,
            database = odk_con.db_name
        )
        curs = connection.cursor()
        cursGetTbl = connection.cursor()
        curGetUpdate = connection.cursor()
        cursGetCol = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Initial table name
        odk_table_name = '%s_CORE' % odk_con.odk_table_name.upper().replace('_','')

        # Get Column name and type
        colnames, coltypes = [], []
        cursGetCol.execute("""select * from information_schema.columns
           where table_schema NOT IN ('information_schema', 'pg_catalog')
           and table_name = '%s' order by table_schema, table_name""" % odk_table_name
        )
        for row in cursGetCol:
            colnames.append(row['column_name'])
            coltypes.append(row['data_type'])

        curs.execute("""SELECT * FROM \"%s\".\"%s\"""" % (odk_con.db_schema, odk_table_name))
        all_features = []
        ignored_col = []
        linelen = len(odk_con.geotrace_column) if odk_con.geotrace_column else False
        polygonelen = len(odk_con.geoshape_column) if odk_con.geoshape_column else False
        pointlen = len(odk_con.geopoint_column) if odk_con.geopoint_column else False
        for colname in colnames:
            if linelen and colname[-linelen:] == odk_con.geotrace_column.upper():
                polyline_column = colname
                ignored_col.append(colname)
            elif polygonelen and colname[-polygonelen:] == odk_con.geoshape_column.upper():
                polygon_column = colname
                ignored_col.append(colname)
            elif pointlen and colname[-pointlen-4:-4] == odk_con.geopoint_column.upper():
                if colname[-3:] == 'LAT':
                    latitude_column = colname
                elif colname[-3:] == 'LNG':
                    longitude_column = colname
                elif colname[-3:] == 'ALT':
                    altitude_column = colname
                elif colname[-3:] == 'ACC':
                    accuracy_column = colname
                ignored_col.append(colname)
        for record in curs.fetchall():
            if odk_con.geometry_type == 'polyline':
                geom_idx = colnames.index(polyline_column)
                re_geomerty = record[geom_idx].split(";")
                coordinates_list = []
                properties_dict = {}
                for coordinate in re_geomerty:
                    try:
                        x_coord = coordinate.split(" ")[1]
                        y_coord = coordinate.split(" ")[0]
                        coordinates_list.append((float(x_coord), float(y_coord)))
                        for colname in colnames:
                            if colname not in ignored_col and not colname.startswith('_') and colname != "META_INSTANCE_ID":
                                properties_dict.update({
                                    colname: record[colnames.index(colname)]
                                })
                    except IndexError as error:
                        pass
                read_odk_image(odk_con, properties_dict, record, colnames)
                all_features.append(Feature(
                    geometry=MultiLineString([coordinates_list]),
                    properties=properties_dict
                ))
            elif odk_con.geometry_type == 'polygon':
                geom_idx = colnames.index(polygon_column)
                re_geomerty = record[geom_idx].split(";")
                coordinates_list = []
                properties_dict = {}
                for coordinate in re_geomerty:
                    try:
                        x_coord = coordinate.split(" ")[1]
                        y_coord = coordinate.split(" ")[0]
                        coordinates_list.append((float(x_coord), float(y_coord)))
                        for colname in colnames:
                            if colname not in ignored_col and not colname.startswith('_') and colname != "META_INSTANCE_ID":
                                properties_dict.update({
                                    colname: record[colnames.index(colname)]
                                })
                    except IndexError as error:
                        pass
                read_odk_image(odk_con, properties_dict, record, colnames)
                # Inspection Geo-Intellegent
                coordinates_list_closed = coordinates_list
                coordinates_list_closed.append(coordinates_list[0])
                odkgeom = Polygon((tuple(coordinates_list)))
                earthquake_intensity_result = inspect_earthquake_intensity(
                    odkgeom,
                    properties_dict
                )
                properties_dict.update({
                    "EARTHQUAKE_INTENSITY_RESULT": earthquake_intensity_result
                })
                # Store to feature
                all_features.append(Feature(
                    geometry=PolygonJson([coordinates_list]),
                    properties=properties_dict
                ))
            elif odk_con.geometry_type == 'point':
                lat_idx = colnames.index(latitude_column)
                y_coord = float(record[lat_idx])
                lon_idx = colnames.index(longitude_column)
                x_coord = float(record[lon_idx])
                properties_dict = {}
                for colname in colnames:
                    if colname not in ignored_col and not colname.startswith('_') and colname != "META_INSTANCE_ID":
                        properties_dict.update({
                            colname: record[colnames.index(colname)]
                        })
                read_odk_image(odk_con, properties_dict, record, colnames)
                properties_dict.update({
                    'ALTITUDE': float(record[colnames.index(altitude_column)]),
                    'ACCURACY': float(record[colnames.index(accuracy_column)])
                })
                # Inspection Geo-Intellegent
                odkgeom = Point((x_coord, y_coord)),
                earthquake_intensity_result = inspect_earthquake_intensity(
                    odkgeom,
                    properties_dict
                )
                properties_dict.update({
                    "EARTHQUAKE_INTENSITY_RESULT": earthquake_intensity_result
                })
                # Store to feature
                all_features.append(Feature(
                    geometry=PointJson((x_coord, y_coord)),
                    properties=properties_dict
                ))

        feature_collection = FeatureCollection(all_features)
        return feature_collection
    except (Exception, psycopg2.Error) as error:
        print ("Error in progress:", error)
