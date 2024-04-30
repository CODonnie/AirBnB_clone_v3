#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a JSON-formatted 404 status code response
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

