#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.inspection import Inspection
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/inspections', methods=['GET'], strict_slashes=False)
def get_inspections():
    """
    Retrieves the list of all inspection objects
    or a specific inspection
    """
    all_inspections = storage.all('Inspection').values()
    list_inspections = []
    for inspection in all_inspections:
        list_inspections.append(inspection.to_dict())
    return jsonify(list_inspections)


@app_views.route('/inspections/<inspection_id>', methods=['GET'], strict_slashes=False)
def get_inspection(inspection_id):
    """ Retrieves an inspection """
    inspection = storage.get('Inspection', inspection_id)
    if not inspection:
        abort(404)

    return jsonify(inspection.to_dict())


@app_views.route('/inspections/<inspection_id>', methods=['DELETE'],
                 strict_slashes=False)
@token_required
def delete_inspection(inspection_id):
    """
    Deletes a inspection Object
    """

    inspection = storage.get('Inspection', inspection_id)

    if not inspection:
        abort(404)

    storage.delete(inspection)
    storage.save()

    return make_response(jsonify({"message": "Deleted Successfully!"}), 200)


@app_views.route('/inspections', methods=['POST'], strict_slashes=False)
@token_required
def post_inspection():
    """
    Creates a inspection
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'hive_id' not in request.get_json():
        abort(400, description="Missing Beehive ID")
    if 'observations' not in request.get_json():
        abort(400, description="Missing observations")

    data = request.get_json()
    # check if the beehive exists
    if storage.get('Beehive', data.get('hive_id')) is None:
        abort(400, description="Beehive does not exist")

    new_inspection = Inspection(**data)
    new_inspection.save()
    return make_response(jsonify(new_inspection.to_dict()), 201)


@app_views.route('/inspections/<inspection_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_inspection(inspection_id):
    """
    Updates a inspection
    """
    inspection = storage.get('Inspection', inspection_id)

    if not inspection:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id','created_at', 'hive_id', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(inspection, key, value)
    storage.save()
    return make_response(jsonify(inspection.to_dict()), 200)
