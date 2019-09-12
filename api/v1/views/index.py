#!/usr/bin/python3
"""Module to create a flask route"""
from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint
from models import storage

clsDict = {
    "Amenity": "amenities",
    "City": "cities",
    "Place": "places",
    "Review": "reviews",
    "State": "states",
    "User": "users"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def num_objects():
    """Returns the number of objects by type"""
    newDict = {}
    for k, v in clsDict.items():
        newDict[k] = storage.count(v)
    return jsonify(newDict)


if __name__ == "__main__":
    pass
