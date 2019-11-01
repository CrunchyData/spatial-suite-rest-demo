import os
import json
import psycopg2
from flask_restful import reqparse, Api, Resource
from flask import Flask

# Setup the Flask application.

app = Flask(__name__)
api = Api(app)


# Making sure everything works
class HelloWorld(Resource):
    def get(self):
        return "Hello World"


api.add_resource(HelloWorld, '/')


class FireHazardStatus(Resource):
    def get(self, parcelid):
        print(os.getenv('db_username') + " " + os.getenv('FIREDATA_PGBOUNCER_SERVICE_HOST') + " " + os.getenv('db_password'))
        conn = psycopg2.connect(database='firedata', user=os.getenv('db_username'),
                                    host=os.getenv('FIREDATA_PGBOUNCER_SERVICE_HOST'),
                                    password=os.getenv('db_password'))
        cur = conn.cursor()
        cur.execute("""select gid, ST_AsText(geom) as geom from assessor_parcels LIMIT 3""")

        rows = cur.fetchall()
        result_string = "<h2>Here are your results: </h2>"
        for row in rows:
            result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + "</h3>"

        cur.close()
        conn.close()

        return result_string


api.add_resource(FireHazardStatus, '/parcel/firehazard/', '/parcel/firehazard/<int:parcelid>')
