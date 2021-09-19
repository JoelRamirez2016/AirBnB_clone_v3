#!/usr/bin/python3
"""define routes for api cities"""
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=["GET"])
def city_places(city_id):
    """Retrieves all places from a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = list(map(lambda x: x.to_dict(), city.places))
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=["GET"])
def place_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if (place):
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(City, place_id)
    if (place):
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_json = None
    try:
        place_json = request.get_json()
    except Exception:
        pass
    if not place_json:
        return 'Not a JSON', 400
    if 'name' not in place_json:
        return 'Missing name', 400
    if 'user_id' not in place_json:
        return 'Missing user_id', 400
    user = storage.get(User, place_json['user_id'])
    if not user:
        abort(404)
    place_json['city_id'] = city_id
    place = Place(**place_json)
    place.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """Updates a city object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
