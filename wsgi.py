import os
import json
import psycopg2
from flask import Flask, request, jsonify

# Setup the Flask application.

app = Flask(__name__)

def get_connection():
    conn = psycopg2.connect(database='firedata', user=os.getenv('db_username'),
                            host=os.getenv('FIREDATA_PGBOUNCER_SERVICE_HOST'),
                            password=os.getenv('db_password'))

    return conn

# This connection is read only so let's get the data from the replica
def get_tiger_connection():
    conn = psycopg2.connect(database='tiger', user=os.getenv('db_username'),
                            host=os.getenv('FIREDATA_REPLICA_SERVICE_HOST'),
                            password=os.getenv('db_password'))

    return conn


@app.route('/')
def index():
    return "Hello World"

@app.route('/geocode/<string:address>', methods=['GET'])
def geocode_function(address):
    result = {}

    tiger_conn = get_tiger_connection()
    tiger_cur = tiger_conn.cursor()

    conn = get_connection()
    cur = conn.cursor()

    #do the geocode on the address
    geocode_sql = "select ST_X(g.geomout) as lon, ST_Y(g.geomout) as lat, g.geomout as wkb from tiger.geocode('{add}') as g".format(add=address)
    tiger_cur.execute(geocode_sql)
    rows = tiger_cur.fetchall()
    print(rows)
    result['lon'] = rows[0]
    result['lat'] = rows[1]

    #then take the wkb and use it to get the parcel id
    parcel_sql = "select gid from assessor_parcels where st_intersects( geom, st_transform('{geom}'::geometry, 2227))".format(geom=rows[0])
    cur.execute(parcel_sql)
    parcel_rows = cur.fetchall
    result['parcelid'] = parcel_rows[0]

    cur.close()
    tiger_cur.close()
    conn.close()
    tiger_conn.close()

    return result


@app.route('/notify/parcel-and-distance', methods=['GET'])
def notify_function():

    #TODO should test for parameter passing
    parcelid  = request.args.get('parcelid', type=int)
    distance = request.args.get('dist', type=int)

    conn = get_connection()
    cur = conn.cursor()
    sql_string = "SELECT st_astext( ST_Transform(a.geom, 4326)), a.gid, (a.sitnumber || ' ' ||  a.sitstreet || ', ' ||  a.sitcity || ' ' || a.sitzip) as address, a.acres " \
                 "FROM assessor_parcels a JOIN assessor_parcels b ON ST_DWithin(a.geom, b.geom, {radius}) WHERE b.gid = {id}".format(id=parcelid, radius=distance)
    cur.execute(sql_string)
    rows = cur.fetchall()

    results = []

    for row in rows:
        result = {"parcelid": str(row[1]), "address": row[2], "acres": row[3], "geom": row[0]}
        results.append(result)

    return jsonify(results)


@app.route('/parcel/firehazard/<int:parcelid>', methods=['GET', 'PUT'])
def get_firehazard(parcelid):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        sql_string = "select gid, firehazard from assessor_parcels where gid =  {id}".format(id=parcelid)
        cur.execute(sql_string)

        rows = cur.fetchall()
        for row in rows:
            result = { "parcelid": row[0], "firehazard": str(row[1])}

        cur.close()
        conn.close()
        return result

    elif request.method == 'PUT':
        json_response = request.get_json()
        new_firehazard = json_response['firehazard']


        sql = """ update assessor_parcels SET firehazard =  %s WHERE gid  = %s"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (new_firehazard, parcelid))
        conn.commit()
        cur.close()
        conn.close()
        return {"result": "success"}


    cur.close()
    conn.close()

