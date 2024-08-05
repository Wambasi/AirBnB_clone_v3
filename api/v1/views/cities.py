#!/usr/bin/python3
"""This module creates a new view for city objects"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


# Retrieves the list of all City objects: GET /api/v1/states/<state_id>/cities
@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """This function retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


# Retrieves a City object. : GET /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """This function retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


# Deletes a City object: DELETE /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """This function deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200  # deleted successfully


# Creates a City: POST /api/v1/states/<state_id>/cities
@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """This function creates a new City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    # store json data from request in a variable
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)  # creates a new city using dict unpacking
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


# Updates a City object: PUT /api/v1/cities/<city_id>
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """This function updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    # store json data from request in a variable
    data = request.get_json()
    # update city object
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
