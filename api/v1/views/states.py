#!/usr/bin/python3
"""define routes for api states"""
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False, methods=["GET"])
def states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states = list(map(lambda x: x.to_dict(), states))
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def states_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if (state):
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def create_state():
    """Creates a new State"""
    state_json = None
    try:
        state_json = request.get_json()
    except Exception:
        pass
    if not state_json:
        return 'Not a JSON', 400
    if 'name' not in state_json:
        return 'Missing name', 400
    state = State(**state_json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=["DELETE"])
def states_id_delete(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if (state):
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def state_id_put(state_id):
    """Updates a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    if 'id' in json_data:
        json_data.pop('id')
    if 'created_at' in json_data:
        json_data.pop('created_at')
    if 'updated_at' in json_data:
        json_data.pop('updated_at')
    for key, value in json_data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
