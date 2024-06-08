#!/usr/bin/python3
"""Create Blueprints"""
from flask import Blueprint


views = Blueprint('views', __name__, url_prefix='/')

# import all the blueprints
from web.views.index import *
from web.views.apiary import *
from web.views.beehive import *
