import psycopg2
import psycopg2.extras

from geojson import MultiLineString, Point, Feature, FeatureCollection

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

        # Get Column name and type
        colnames, coltypes = [], []
        cursGetCol.execute("""select * from information_schema.columns
           where table_schema NOT IN ('information_schema', 'pg_catalog')
           and table_name = '%s' order by table_schema, table_name""" % odk_con.odk_table_name
        )
        for row in cursGetCol:
            colnames.append(row['column_name'])
            coltypes.append(row['data_type'])

        curs.execute("""SELECT * FROM \"%s\".\"%s\"""" % (odk_con.db_schema, odk_con.odk_table_name))
        all_features = []
        ignored_col = [
            odk_con.polyline_column,
            odk_con.polygon_column,
            odk_con.latitude_column,
            odk_con.longitude_column
        ]
        for record in curs.fetchall():
            if odk_con.geometry_type == 'polyline':
                geom_idx = colnames.index(odk_con.polyline_column)
                re_geomerty = record[geom_idx].split(";")
                coordinates_list = []
                properties_dict = {}
                for coordinate in re_geomerty:
                    try:
                        x_coord = coordinate.split(" ")[1]
                        y_coord = coordinate.split(" ")[0]
                        coordinates_list.append((float(x_coord), float(y_coord)))
                        for colname in colnames:
                            if colname not in ignored_col:
                                properties_dict.update({
                                    colname: record[colnames.index(colname)]
                                })
                    except IndexError as error:
                        pass
                all_features.append(Feature(
                    geometry=MultiLineString([coordinates_list]),
                    properties=properties_dict
                ))
            elif odk_con.geometry_type == 'point':
                lat_idx = colnames.index(odk_con.latitude_column)
                y_coord = float(record[lat_idx])
                lon_idx = colnames.index(odk_con.longitude_column)
                x_coord = float(record[lon_idx])
                properties_dict = {}
                for colname in colnames:
                    if colname not in ignored_col:
                        properties_dict.update({
                            colname: record[colnames.index(colname)]
                        })
                all_features.append(Feature(
                    geometry=Point((x_coord, y_coord)),
                    properties=properties_dict
                ))
        feature_collection = FeatureCollection(all_features)
        return feature_collection
    except (Exception, psycopg2.Error) as error:
        print ("Error in progress:", error)
