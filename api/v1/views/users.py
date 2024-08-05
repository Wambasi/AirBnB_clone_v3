#!/usr/bin/python3
"""This module creates a new view for user objects"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from flask import jsonify, abort, request


# Retrieves the list of all User objects: GET /api/v1/users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    This function retrieves a list of all User objects
    it defines a GET request to endpoint /users
    """
    # retrieve all User objects
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list), 200


# Retrieves a User object: GET /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    This function retrieves a User object by its id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


# Deletes a User object: DELETE /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """This function deletes a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    # it returns 200 ok meaning successfull deletion
    return jsonify({}), 200


# Creates a User: POST /api/v1/users
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """This function creates a new User"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    user = User(**user_json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


# Updates a User object: PUT /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """This function updates a User object"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in user_json.items():
        # Ignore keys: id, email, created_at and updated_at
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
