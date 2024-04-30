#!/usr/bin/python3
"""
Amenity API view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage
from flasgger.utils import swag_from

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>/', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def create_amenity():
    """
    Creates an Amenity
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Not a JSON or Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
