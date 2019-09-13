#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def placeGetter(city_id):
    """Get all places in a city"""
    City = models.storage.get("City", city_id)
    if City is None:
        abort(404)
    places = []
    for thing in City.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def placeSelector(place_id):
    """Get place information by id"""
    place = models.storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    """Make a new place"""
    City = models.storage.get("City", city_id)
    if City is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    kwargs = request.get_json()
    if "user_id" not in kwargs:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    User = models.storage.get("User", kwargs["user_id"])
    if User is None:
        abort(404)
    if "name" not in kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)
    kwargs["city_id"] = city_id
    Place = Place(**kwargs)
    Place.save()
    return make_response(jsonify(Place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """Delete a place by id"""
    kill = models.storage.get("Place", place_id)
    if kill is None:
        abort(404)
    kill.delete()
    models.storage.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def putPlace(place_id):
    """Update a place by id"""
    update = models.storage.get("Place", place_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at",
                       "updated_at"]:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())
