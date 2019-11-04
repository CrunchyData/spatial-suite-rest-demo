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


@app.route('/')
def index():
    return "Hello World"

@app.route('/notify/parcel-and-distance', methods=['GET'])
def notify_function():

    #TODO should test for parameter passing
    parcelid  = request.args.get('parcelid', type=int)
    distance = request.args.get('dist', type=int)

    conn = get_connection()
    cur = conn.cursor()
    sql_string = "SELECT st_astext( ST_Transform(a.geom, 4326)), a.gid (sitnumber || ' ' ||  sitstreet || ', ' ||  sitcity || ' ' || sitzip) as address, acres " \
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

        return result

    elif request.method == 'PUT':
        json_response = request.get_json()
        new_firehazard = json_response['firehazard']


        sql = """ update assessor_parcels SET firehazard =  %s WHERE gid  = %s"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, (new_firehazard, parcelid))
        conn.commit()
        return {"result": "success"}


    cur.close()
    conn.close()

