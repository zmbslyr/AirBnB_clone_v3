#!/usr/bin/python3
"""Module to create flask app"""
from models import storage
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Method to close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
        port=os.getenv("HBNB_SPI_PORT", "5000"),
        threaded=True)
