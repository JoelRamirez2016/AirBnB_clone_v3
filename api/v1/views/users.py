#!/usr/bin/python3
"""define routes for api users"""
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', strict_slashes=False, methods=["GET"])
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    users = list(map(lambda x: x.to_dict(), users))
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """Retrieves an user object"""
    user = storage.get(User, user_id)
    if (user):
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["DELETE"])
def delele_user(user_id):
    """Deletes an User object"""
    user = storage.get(User, user_id)
    if (user):
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=["POST"])
def create_user():
    """Creates a new User"""
    user_json = None
    try:
        user_json = request.get_json()
    except Exception:
        pass
    if not user_json:
        return 'Not a JSON', 400
    if 'name' not in user_json:
        return 'Missing name', 400
    if 'password' not in user_json:
        return 'Missing password', 400
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    json_data = None
    json_data = request.get_json()
    if not json_data:
        return 'Not a JSON', 400
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
