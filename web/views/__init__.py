#!/usr/bin/python3
"""Create Blueprints"""
from flask import Blueprint


views = Blueprint('views', __name__, url_prefix='/')

# import all the blueprints
from web.views.index import *
from web.views.apiary import *
from web.views.beehive import *
from web.views.auth import *
from web.views.inspection import *
from web.views.harvest import *
