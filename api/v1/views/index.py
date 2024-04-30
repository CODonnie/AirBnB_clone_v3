#!/usr/bin/python3
"""
Index view for API v1
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the API
    """
    return jsonify({"status": "OK"})
