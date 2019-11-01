import os
import json
import psycopg2
from flask import Flask, request

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


@app.route('/parcel/firehazard/<int:parcelid>', methods=['GET'])
def get_firehazard(parcelid):
    conn = get_connection()
    cur = conn.cursor()
    sql_string = "select gid, firehazard from assessor_parcels where gid = '%s'" % (parcelid)
    cur.execute(sql_string)

    rows = cur.fetchall()
    for row in rows:
        result = { "parcelid": row[0], "firehazard": str(row[1])}

    return result

    cur.close()
    conn.close()

@app.route('/parcel/firehazard/', methods=['PUT'])
def update_firehazard():

    #get the JSON payload
    json_response = request.get_json()
    parcelid = json_response['parcelid']
    new_firehazard = json_response['firehazard']


    sql = """ update assessor_parcels SET firehazard =  %s WHERE gid  = %s"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (new_firehazard, parcelid))
    conn.commit()
    cur.close()
    conn.close()
    return {"result": "success"}