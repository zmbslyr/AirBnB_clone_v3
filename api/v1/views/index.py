#!/usr/bin/python3
"""Module to create a flask route"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def num_objects():
    """Returns the number of objects by type"""
    clsDict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    newDict = {}
    for k, v in clsDict.items():
        newDict[k] = models.storage.count(v)
    return jsonify(newDict)
