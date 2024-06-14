#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.harvest import Harvest
from models import storage
from api.v1.views import app_views
from decorators import token_required
from flask import abort, jsonify, make_response, request


@app_views.route('/harvests', methods=['GET'], strict_slashes=False)
def get_harvests():
    """
    Retrieves the list of all harvest objects
    or a specific harvest
    """
    all_harvests = storage.all('Harvest').values()
    list_harvests = []
    for harvest in all_harvests:
        list_harvests.append(harvest.to_dict())
    return jsonify(list_harvests)


@app_views.route('/harvests/<harvest_id>', methods=['GET'], strict_slashes=False)
def get_harvest(harvest_id):
    """ Retrieves an harvest """
    harvest = storage.get('Harvest', harvest_id)
    if not harvest:
        abort(404)

    return jsonify(harvest.to_dict())


@app_views.route('/harvests/<harvest_id>', methods=['DELETE'],
                 strict_slashes=False)
@token_required
def delete_harvest(current_user, harvest_id):
    """
    Deletes a harvest Object
    """

    harvest = storage.get('Harvest', harvest_id)

    if not harvest:
        abort(404)

    storage.delete(harvest)
    storage.save()

    return make_response(jsonify({"message": "Deleted successfully"}), 200)


@app_views.route('/harvests', methods=['POST'], strict_slashes=False)
@token_required
def post_harvest(current_user):
    """
    Creates a harvest
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'hive_id' not in request.get_json():
        abort(400, description="Missing Beehive ID")
    if 'quantity' not in request.get_json():
        abort(400, description="Missing quantity")

    data = request.get_json()
    # check if the beehive exists
    if storage.get('Beehive', data.get('hive_id')) is None:
        abort(400, description="Beehive does not exist")
    new_harvest = Harvest(**data)
    new_harvest.save()
    return make_response(jsonify(new_harvest.to_dict()), 201)


@app_views.route('/harvests/<harvest_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_harvest(current_user, harvest_id):
    """
    Updates a harvest
    """
    harvest = storage.get('Harvest', harvest_id)

    if not harvest:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(harvest, key, value)
    storage.save()
    return make_response(jsonify(harvest.to_dict()), 200)
