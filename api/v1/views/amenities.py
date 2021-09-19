#!/usr/bin/python3
"""define routes for api amenities"""
from flask import jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=["GET"])
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["GET"])
def get_amenity(amenity_id):
    """Retrieves an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["DELETE"])
def delele_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity):
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=["POST"])
def create_amenity():
    """Creates a new Amenity"""
    amenity_json = None
    try:
        amenity_json = request.get_json()
    except Exception:
        pass
    if not amenity_json:
        return 'Not a JSON', 400
    if 'name' not in amenity_json:
        return 'Missing name', 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    """Updates a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
