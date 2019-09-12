#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getStateCities(state_id):
    """return cities in a given state"""
    cityList = []
    State = models.storage.get('State', state_id)
    if State is None:
        abort(404)
    Allcity = models.storage.all(City)
    for city in Allcity.values():
        if city.state_id == state_id:
            cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postCity(state_id):
    """make a city and add it to db"""
    if models.storage.get("State", state_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    makeCity = City(**request.get_json())
    setattr(makeCity, "state_id", state_id)
    makeCity.save()
    return make_response(jsonify(makeCity.to_dict()), 201)
