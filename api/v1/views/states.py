#!/usr/bin/python3
"""Module to create a flask route"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states' methods=['GET'])
def get_state():
    return json.dumps([state.to_dict()
        for state in models.storage.all('State').values()])

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    temp = models.storage.get('State', state_id)
    if temp is None:
        abort(404)
    else:
        temp.delete()
        return '{}'

@app_views.route('/states', methods=['POST'])
def create_state():
    """ creates a new state object. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, '{"error": "Not a JSON"}')
    if 'name' not in body:
        abort(400, '{"error": "Missing name"}')
    state = models.state.State(**body)
    models.storage.new(state)
    models.storage.save()
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update specific state object with new information. """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, '{"error":"Not a JSON"}')
    state = models.storage.get('State', state_id)
    if state is None:
        abort(404)
    for key, value in body.items():
        if key not in ('created_at', 'updated_at', 'id'):
            setattr(state, key, value)
    return jsonify(state.to_dict())
