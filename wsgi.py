import os
import json
from flask_restful import reqparse, Api, Resource

from flask import Flask

# Setup the Flask application.

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(Resource):
        return "Hello World"

api.add_resource(HelloWorld, '/')