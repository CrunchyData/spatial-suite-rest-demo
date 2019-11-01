import os
import json
import psycopg2
from flask import Flask, request

# Setup the Flask application.

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/parcel/firehazard/<int:parcelid>')
def firehazard(parcelid):
    conn = psycopg2.connect(database='firedata', user=os.getenv('db_username'),
                            host=os.getenv('FIREDATA_PGBOUNCER_SERVICE_HOST'),
                            password=os.getenv('db_password'))
    cur = conn.cursor()
    if request.method == 'GET':
        sql_string = "select gid, firehazard from assessor_parcels where gid = '%s'" % (parcelid)
        cur.execute(sql_string)

        rows = cur.fetchall()
        for row in rows:
            result = { "parcelid": row[0], "firehazard": str(row[1])}

        return result
    elif request.method == 'PUT':
        return 'json'

    return "We Weren't Supposed To Be Called The Way You Did"

    cur.close()
    conn.close()
