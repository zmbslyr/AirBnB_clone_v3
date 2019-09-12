#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getStateCities(state_id):
    """return cities in a given state"""
    Allcity = []
    State = models.storage.get('State', state_id)
    if State is None:
        abort(404)
    else:
        Allcity.append(city.to_dict() for city in State.cities)
    return jsonify(Allcity)
