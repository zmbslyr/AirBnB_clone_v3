#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def userGetter():
    """Gets info from all users"""
    Users = []
    for thing in models.storage.all("User").values():
        Users.append(thing.to_dict())
    return jsonify(Users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def user_id_Getter(user_id):
    """Get info about a user by id"""
    id = models.storage.get("User", user_id)
    if id is None:
        abort(404)
    return jsonify(id.to_dict())


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def userPost():
    """Make a new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    newUser = User(**request.get_json())
    newUser.save()
    return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def userKill(user_id):
    """Deletes a user by their id"""
    kill = models.storage.get("User", user_id)
    if Kill is None:
        abort(404)
    kill.delete()
    models.storage.save()
    return (jsonify({}))


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def userUpdate(user_id):
    """Update a user based on id"""
    update = models.storage.get("User", user_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())
