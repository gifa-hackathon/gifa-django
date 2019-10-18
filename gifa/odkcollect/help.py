import psycopg2
import psycopg2.extras

from django.conf import settings
from django.db import connection
from django.contrib.gis.geos import Point, Polygon, LineString

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


def inspect_flood(odkgeom, properties_dict):
    """
    Inspect ODK object based on flood submersion
    """
    intersaction_list = RendamanBanjir.objects.filter(polygon__intersects=odkgeom)
    if intersaction_list:
        info_statement = "<p>Berdasarkan data rendaman banjir Baleendah, lokasi ini bersinggungan dengan wilayah terdampak banjir</p>"
    else:
        info_statement = "<p>Lokasi ini diluar data rendaman banjir</p>"
    return info_statement


def inspect_earthquake_intensity(odkgeom, properties_dict):
    """
    Inspect ODK object based on earthquake intensity data
    """
    intersaction_list = IntensitasGempa.objects.filter(polygon__intersects=odkgeom)
    if intersaction_list:
        mi_value = intersaction_list[0].value
        if mi_value <= 2:
            mmi = 'I'
        elif mi_value > 2 and mi_value <= 3:
            mmi = 'II'
        elif mi_value > 3 and mi_value <= 3.5:
            mmi = 'III'
        elif mi_value > 3.5 and mi_value <= 4:
            mmi = 'IV'
        elif mi_value > 4 and mi_value <= 4.5:
            mmi = 'V'
        elif mi_value > 4.5 and mi_value <= 5:
            mmi = 'VI'
        elif mi_value > 5 and mi_value <= 5.5:
            mmi = 'VII'
        elif mi_value > 5.5 and mi_value <= 6:
            mmi = 'VIII'
        elif mi_value > 6 and mi_value <= 6.5:
            mmi = 'IX'
        elif mi_value > 6.5 and mi_value <= 7:
            mmi = 'X'
        elif mi_value > 7 and mi_value <= 7.5:
            mmi = 'XI'
        elif mi_value > 7.5:
            mmi = 'XII'
        else:
            mmi = 'UNKNOWN'
        stmpart = "Berdasarkan data intensitas gempa, lokasi ini berada pada wilayah dengan magnitudo"
        unit = "SR"
        stmpart3 = "atau skala"
        bmkg_mmi = "<a href='https://www.bmkg.go.id/gempabumi/skala-mmi.bmkg' target='_blank'>%s</a> MMI" % mmi
        info_statement = "<p>%s <strong>%s %s</strong>, %s %s</p>" % (
            stmpart,
            intersaction_list[0].value,
            unit,
            stmpart3,
            bmkg_mmi
        )
    else:
        info_statement = "<p>Lokasi ini diluar data intensitas gempa</p>"
    return info_statement


def distance_to_lembangfault(odkgeom, properties_dict, point):
    """
    Measure distance between ODK object to lembang fault
    """
    cursor = connection.cursor()
    odkgeom = odkgeom[0] if point else odkgeom
    cursor.execute("SELECT ST_Distance(ST_Transform('%s'::geometry, 3857), ST_Transform((select polyline from dashboard_sesarlembang)::geometry, 3857));" % odkgeom)
    shortest_distance = cursor.fetchall()
    statement = "<p>Berdasarkan data sesar lembang, jarak lokasi ini ke sesar lembang adalah <b>%s Meter</b></p>" % (
        round(shortest_distance[0][0], 3)
    )
    return statement


def read_odk_image(odk_con, properties_dict, record, colnames):
    """
    Read ODK Image and put inside properties
    """
    image_columns = [i.strip() for i in odk_con.geometry_image.split(";")]

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
        odk_table_name = '%s_CORE' % odk_con.odk_table_name.upper()

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
        # linelen = len(odk_con.geotrace_column) if odk_con.geotrace_column else False
        # polygonelen = len(odk_con.geoshape_column) if odk_con.geoshape_column else False
        # pointlen = len(odk_con.geopoint_column) if odk_con.geopoint_column else False
        for colname in colnames:
            if colname == "%s_%s" % (odk_con.group_column.upper(), odk_con.geometry_column.upper()):
                polyline_column = colname
                ignored_col.append(colname)
            # elif polygonelen and colname[-polygonelen:] == odk_con.geoshape_column.upper():
            #     polygon_column = colname
            #     ignored_col.append(colname)
            # elif pointlen and colname[-pointlen-4:-4] == odk_con.geopoint_column.upper():
            #     if colname[-3:] == 'LAT':
            #         latitude_column = colname
            #     elif colname[-3:] == 'LNG':
            #         longitude_column = colname
            #     elif colname[-3:] == 'ALT':
            #         altitude_column = colname
            #     elif colname[-3:] == 'ACC':
            #         accuracy_column = colname
            #     ignored_col.append(colname)
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
                # Inspection Geo-Intellegent
                odkgeom = LineString((tuple(coordinates_list)))
                earthquake_intensity_result = inspect_earthquake_intensity(
                    odkgeom,
                    properties_dict
                )
                inspect_flood_result = inspect_flood(
                    odkgeom,
                    properties_dict
                )
                distance_to_fault_result = distance_to_lembangfault(
                    odkgeom,
                    properties_dict,
                    False
                )
                properties_dict.update({
                    "EARTHQUAKE_INTENSITY_RESULT": earthquake_intensity_result,
                    "INSPECT_FLOOD_RESULT": inspect_flood_result,
                    "DISTANCE_TO_FAULT_RESULT": distance_to_fault_result
                })
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
                odkgeom = Polygon((tuple(coordinates_list_closed)))
                earthquake_intensity_result = inspect_earthquake_intensity(
                    odkgeom,
                    properties_dict
                )
                inspect_flood_result = inspect_flood(
                    odkgeom,
                    properties_dict
                )
                distance_to_fault_result = distance_to_lembangfault(
                    odkgeom,
                    properties_dict,
                    False
                )
                properties_dict.update({
                    "EARTHQUAKE_INTENSITY_RESULT": earthquake_intensity_result,
                    "INSPECT_FLOOD_RESULT": inspect_flood_result,
                    "DISTANCE_TO_FAULT_RESULT": distance_to_fault_result
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
                inspect_flood_result = inspect_flood(
                    odkgeom,
                    properties_dict
                )
                distance_to_fault_result = distance_to_lembangfault(
                    odkgeom,
                    properties_dict,
                    True
                )
                properties_dict.update({
                    "EARTHQUAKE_INTENSITY_RESULT": earthquake_intensity_result,
                    "INSPECT_FLOOD_RESULT": inspect_flood_result,
                    "DISTANCE_TO_FAULT_RESULT": distance_to_fault_result
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
