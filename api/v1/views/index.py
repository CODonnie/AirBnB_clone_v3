#!/usr/bin/python3
"""
Index view for API v1
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Returns the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each object by type
    """
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
