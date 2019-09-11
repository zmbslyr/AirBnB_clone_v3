#!/usr/bin/python3
"""Module to create a flask route"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route("/status")
def status():
    """Returns a JSON status"""
    return jsonify(status="OK")
