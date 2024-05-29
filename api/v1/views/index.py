#!/usr/bin/python3
""" Index """
from models.beehive import Beehive
from models.harvest import Harvest
from models.inspection import Inspection
from models.apiary import Apiary
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = [Beehive, Harvest, Inspection, User, Apiary]
    names = ["beehives", "harvests", "inspections", "users", "apiaries"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
