#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.apiary import Apiary
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/apiaries', methods=['GET'], strict_slashes=False)
def get_apiaries():
    """
    Retrieves the list of all apiary objects
    or a specific apiary
    """
    all_apiaries = storage.all('Apiary').values()
    list_apiaries = []
    for apiary in all_apiaries:
        list_apiaries.append(apiary.to_dict())
    return jsonify(list_apiaries)


@app_views.route('/apiaries/<apiary_id>', methods=['GET'], strict_slashes=False)
def get_apiary(apiary_id):
    """ Retrieves an apiary """
    apiary = storage.get('Apiary', apiary_id)
    if not apiary:
        abort(404)

    return jsonify(apiary.to_dict())


@app_views.route('/apiaries/<apiary_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_apiary(apiary_id):
    """
    Deletes a apiary Object
    """

    apiary = storage.get('Apiary', apiary_id)

    if not apiary:
        abort(404)

    storage.delete(apiary)
    storage.save()

    return make_response(jsonify({"message": "Deleted successfully!"}), 200)


@app_views.route('/apiaries', methods=['POST'], strict_slashes=False)
def post_apiary():
    """
    Creates a apiary
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_apiary = Apiary(**data)
    new_apiary.save()
    return make_response(jsonify(new_apiary.to_dict()), 201)


@app_views.route('/apiaries/<apiary_id>', methods=['PUT'], strict_slashes=False)
def put_apiary(apiary_id):
    """
    Updates a apiary
    """
    apiary = storage.get('Apiary', apiary_id)

    if not apiary:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(apiary, key, value)
    storage.save()
    return make_response(jsonify(apiary.to_dict()), 200)
