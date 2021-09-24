#!/usr/bin/python3
"""app"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

HBNB_API_HOST = os.getenv('HBNB_API_HOST')
HBNB_API_PORT = os.getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app=app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.errorhandler(404)
def page_not_found(e):
    """return error message for 404"""
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown_db(exeption):
    """Close database"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, port=HBNB_API_PORT or 5000,
            host=HBNB_API_HOST or '0.0.0.0', threaded=True)
