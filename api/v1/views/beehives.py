#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.beehive import Beehive
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/beehives', methods=['GET'], strict_slashes=False)
def get_beehives():
    """
    Retrieves the list of all beehive objects
    or a specific beehive
    """
    all_beehives = storage.all('Beehive').values()
    list_beehives = []
    for beehive in all_beehives:
        list_beehives.append(beehive.to_dict())
    return jsonify(list_beehives)


@app_views.route('/beehives/<beehive_id>', methods=['GET'], strict_slashes=False)
def get_beehive(beehive_id):
    """ Retrieves an beehive """
    beehive = storage.get('Beehive', beehive_id)
    if not beehive:
        abort(404)

    return jsonify(beehive.to_dict())


@app_views.route('/beehives/<beehive_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_beehive(beehive_id):
    """
    Deletes a beehive Object
    """

    beehive = storage.get('Beehive', beehive_id)

    if not beehive:
        abort(404)

    storage.delete(beehive)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/beehives', methods=['POST'], strict_slashes=False)
def post_beehive():
    """
    Creates a beehive
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_beehive = Beehive(**data)
    new_beehive.save()
    return make_response(jsonify(new_beehive.to_dict()), 201)


@app_views.route('/beehives/<beehive_id>', methods=['PUT'], strict_slashes=False)
def put_beehive(beehive_id):
    """
    Updates a beehive
    """
    beehive = storage.get('Beehive', beehive_id)

    if not beehive:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(beehive, key, value)
    storage.save()
    return make_response(jsonify(beehive.to_dict()), 200)
