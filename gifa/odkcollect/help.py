import psycopg2
import psycopg2.extras

from geojson import MultiLineString, Point, Feature, FeatureCollection

def odk_to_json():
    """
    Convert ODK to JSON
    """
    USERNAME = "baleendah_user"
    PASSWORD = "sodagembira"
    HOST = "157.245.194.99"
    PORT = "5432"
    DATABASE = "baleendah"
    TABLE_SCHEMA = "public"

    geomtype = "polyline"
    geomcolmn = "geometri_garis"
    odktable = "fake_odk"

    try:
        # Connect Databases
        connection = psycopg2.connect(
            user = USERNAME,
            password = PASSWORD,
            host = HOST,
            port = PORT,
            database = DATABASE
        )
        curs = connection.cursor()
        cursGetTbl = connection.cursor()
        curGetUpdate = connection.cursor()
        cursGetCol = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Get Column name and type
        colnames, coltypes = [], []
        cursGetCol.execute("""select * from information_schema.columns
           where table_schema NOT IN ('information_schema', 'pg_catalog')
           and table_name = '%s' order by table_schema, table_name""" % odktable
        )
        for row in cursGetCol:
            colnames.append(row['column_name'])
            coltypes.append(row['data_type'])

        curs.execute("""SELECT * FROM \"%s\".\"%s\"""" % (TABLE_SCHEMA, odktable))
        all_features = []
        for record in curs.fetchall():
            geom_idx = colnames.index(geomcolmn)
            re_geomerty = record[geom_idx].split(";")
            if geomtype == 'polyline':
                coordinates_list = []
                properties_dict = {}
                for coordinate in re_geomerty:
                    try:
                        x_coord = coordinate.split(" ")[1]
                        y_coord = coordinate.split(" ")[0]
                        coordinates_list.append((float(x_coord), float(y_coord)))
                        for colname in colnames:
                            if colname != geomcolmn:
                                properties_dict.update({
                                    colname: record[colnames.index(colname)]
                                })
                    except IndexError as error:
                        pass
                all_features.append(Feature(
                    geometry=MultiLineString([coordinates_list]),
                    properties=properties_dict
                ))
        feature_collection = FeatureCollection(all_features)
        return feature_collection
    except (Exception, psycopg2.Error) as error:
        print ("Error in progress:", error)
