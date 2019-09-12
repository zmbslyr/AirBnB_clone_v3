#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def statesGetter():
    """View all the states"""
    Allstate = []
    for states in storage.all("State").values():
        Allstate.append(states.to_dict())
    return jsonify(Allstate)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def stateGetter(state_id):
    """View a specific state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/', methods=['POST'])
def statePoster():
    """creates a new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def stateUpdater(state_id):
    """Update created state"""
    state_update = storage.get("State", state_id)
    if state_update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_update, key, value)
    state_update.save()
    return jsonify(state_update.to_dict())
