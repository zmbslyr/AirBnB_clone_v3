#!/usr/bin/python3
"""Module to create a flask route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request, Blueprint
import models
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviewGetter(place_id):
    """Get all the reviews"""
    if models.storage.get('Place', place_id) is None:
        abort(404)
    reviews = []
    things = models.storage.all(Review)
    for review in things.values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def reviewSelector(review_id):
    """Gets a review by id"""
    select = models.storage.get("Review", review_id)
    if select is None:
        abort(404)
    return jsonify(select.to_dict())


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def reviewPoster(place_id):
    """Make a new review"""
    if models.storage.get("Place", place_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if type(request.get_json()) is dict:
        if models.storage.get("User", request.get_json()["user_id"]) is None:
            abort(404)
    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)

    review = Review(**request.get_json())
    setattr(review, 'place_id', place_id)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewKiller(review_id):
    """Delete a review based by id"""
    kill = models.storage.get("Review", review_id)
    if kill is None:
        abort(404)
    kill.delete()
    models.storage.save()
    return (jsonify({}))


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviewUpdater(review_id):
    """Update a review by id"""
    update = models.storage.get("Review", review_id)
    if update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at",
                       "updated_at", "place_id", "user_id"]:
            setattr(update, key, value)
    update.save()
    return jsonify(update.to_dict())
