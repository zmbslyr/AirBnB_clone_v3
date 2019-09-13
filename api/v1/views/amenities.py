#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models
from models.amenities import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenityGetter():
    """get all amenities"""
    Alist = []
    for thing in models.storage.all("Amenity").values():
        Alist.append(amenity.to_dict())
    return jsonify(Alist)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenitySelector(amenity_id):
    """select an amenity to get by id"""
    select = models.storage.get("Amenity", amenity_id)
    if select is None:
        abort(404)
    return jsonify(select.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenityPoster():
    """Make a new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(amenityPost.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """Kill an emenity based off of id"""
    kill = models.storage.get("Amenity", amenity_id)
    if kill is None:
        abort(404)
    kill.delete()
    models.storage.save()
    return (jsonify({}))


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putAmenity(amenity_id):
    """update an amenity based off of id"""
    update = models.storage.get("Amenity", amenity_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())
