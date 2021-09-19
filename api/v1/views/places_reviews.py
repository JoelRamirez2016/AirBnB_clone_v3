#!/usr/bin/python3
"""define routes for api places"""
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["GET"])
def place_reviews(place_id):
    """Retrieves all reviews from a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = list(map(lambda x: x.to_dict(), place.reviews))
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["GET"])
def review_id(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if (review):
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Place, review_id)
    if (review):
        storage.delete(review)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["POST"])
def create_review(place_id):
    """Creates a new Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_json = None
    try:
        review_json = request.get_json()
    except Exception:
        pass
    if not review_json:
        return 'Not a JSON', 400
    if 'user_id' not in review_json:
        return 'Missing user_id', 400
    if 'text' not in review_json:
        return 'Missing text', 400
    review_json['place_id'] = place_id
    review = Review(**review_json)
    review.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=["PUT"])
def update_review(review_id):
    """Updates a place object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'place_id',
                       'user_id']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
