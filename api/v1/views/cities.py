#!/usr/bin/python3
"""define routes for api states"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=["GET"])
def state_cities(state_id):
    """Retrieves all cities from a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = list(map(lambda x: x.to_dict(), state.cities))
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["GET"])
def city_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if (city):
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """Creates a new City"""
    state = storage.get(City, state_id)
    if not state:
        abort(404)
    state_json = None
    try:
        state_json = request.get_json()
    except Exception:
        pass
    if not state_json:
        return 'Not a JSON', 400
    if 'name' not in state_json:
        return 'Missing name', 400
    state_json['state_id'] = state_id
    city = City(**state_json)
    city.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """Updates a state object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
