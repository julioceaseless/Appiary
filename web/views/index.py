#!/usr/bin/python3
"""Index endpoint"""

from models import storage
from web.views import views
from os import environ
from flask import render_template
import requests


# retrieve URL for API
API_URL = environ.get('API_URL')

@views.route('/')
def index():
    """Home page"""
    # show stats in dashboard
    try:
        response = requests.get(API_URL)
        data = response.json()
        hives = data.get('beehives')
        apiaries = data.get('apiaries')
        inspections = data.get('inspections')
        harvests = data.get('harvests')
    except Exception as e:
        hives, apiaries, inspections, harvests = ['Error', 'Error', 'Error', 'Error']
    return render_template('index.html', hive_count=hives,
                                         apiary_count=apiaries,
                                         inspect_count=inspections,
                                         harvest_count=harvests)

