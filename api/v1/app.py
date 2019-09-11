#!/usr/bin/python3
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Method to close storage"""
    storage.close()

if __name__ == "__main__":
    app.run(
        host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
        port=os.getenv("HBNB_SPI_PORT", "5000"),
        threaded=True)
