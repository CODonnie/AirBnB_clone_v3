#!/usr/bin/python3
"""
User API view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage
from flasgger.utils import swag_from

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def create_user():
    """
    Creates a User
    """
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Invalid JSON or Missing email/password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
