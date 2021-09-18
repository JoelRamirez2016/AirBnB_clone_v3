#!/usr/bin/python3
"""app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

HBNB_API_HOST = os.getenv('HBNB_API_HOST')
HBNB_API_PORT = os.getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exeption):
    """Close database"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, port=HBNB_API_PORT or 5000,
            host=HBNB_API_HOST or '0.0.0.0', threaded=True)
