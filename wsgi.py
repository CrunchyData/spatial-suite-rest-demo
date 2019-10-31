import os
import json

from flask import Flask

# Setup the Flask application.

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"