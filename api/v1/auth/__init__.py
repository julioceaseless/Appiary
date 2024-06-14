#!/usr/bin/python3
""" Blueprint for Auth endpoints """
from flask import Blueprint


api_auth = Blueprint('api_auth', __name__, url_prefix='/api/v1')

