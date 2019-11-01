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
    def get(Resource):
        return "You got some hazard dude"

api.add_resource(FireHazardStatus, '/parcel/firehazard/<int:parcelid>', '/parcel/firehazard/')
    def get(self, parcelid):
        try:
            conn = psycopg2.connect(database='firedata', user=os.environ.get('db_user'),
                                    host=os.environ.get('FIREDATA_PGBOUNCER_SERVICE_HOST'), password=os.environ.get('db_password'))
        except:

        cur = conn.cursor()
        cur.execute("""select gid, ST_AsText(the_geom) as geom from assessor_parcels LIMIT 3""")

        rows = cur.fetchall()
        result_string = "<h2>Here are your results: </h2>"
        for row in rows:
            result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + "</h3>"

        cur.close()
        conn.close()

        return result_string
        