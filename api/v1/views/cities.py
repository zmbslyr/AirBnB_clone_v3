#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
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
def cityPost(state_id):
    ''' create a new city '''
    if models.storage.get("State", state_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    postit = City(**request.get_json())
    setattr(postit, "state_id", state_id)
    postit.save()
    return make_response(jsonify(postit.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def cityGet(city_id):
    """Get a city from id"""
    grab = storage.get("City", city_id)
    if grab is None:
        abort(404)
    return jsonify(grab.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def cityPut(city_id):
    """update a city"""
    update = models.storage.get("City", city_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cityDelete(city_id):
    """Delete a city based on id"""
    Delete = storage.get("City", city_id)
    if Delete is None:
        abort(404)
    Delete.delete()
    models.storage.save()
    return (jsonify({}))
