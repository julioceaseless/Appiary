#!/usr/bin/python3
'''Start a flask web application'''
from models import storage
from os import environ
from flask import Flask, render_template, request, redirect, url_for
from models.apiary import Apiary
from models.beehive import Beehive
import requests
import uuid

# start flask
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/')
def index():
    """Home page"""
    try:
        response = requests.get("http://127.0.0.1:5000/api/v1/stats")
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

@app.route('/apiaries')
def list_apiaries():
    """List apiaries"""
    apiary_list = []
    apiaries = storage.all('Apiary')
    for apiary_obj in apiaries.values():
        apiary_list.append(f'{apiary_obj.name} - {apiary_obj.id}')
    apiary_list.sort()
    return render_template('list_apiaries.html', apiaries=apiary_list)

@app.route('/apiary/<apiary_id>')
def view_apiary(apiary_id):
    """View apiary"""
    hives_count = 0
    apiary = storage.get('Apiary', apiary_id)
    # count hives in the apiary
    hives = storage.all('Beehive')
    if hives:
        for hive in hives.values():
            if hive.apiary_id == apiary_id:
                hives_count += 1

    return render_template('view_apiary.html', apiary=apiary,
                                               hives_count=hives_count)

@app.route('/apiary/add', methods=['GET', 'POST'])
def add_apiary():
    """Add new apiary"""
    if request.method == 'POST':
        user_id = request.form['user']
        name = request.form['name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        data = {'user_id': user_id,
                'name': name,
                'latitude': latitude,
                'longitude': longitude
                }
        apiary = Apiary(**data)
        apiary.save()
        return redirect(url_for('list_apiaries'))

    users = storage.all('User')
    return render_template('add_apiary.html', users=users)

@app.route('/apiary/delete/<apiary_id>', methods=['GET'])
def delete_apiary(apiary_id):
    """Delete apiary"""
    apiary = storage.get('Apiary', apiary_id)
    storage.delete(apiary)
    storage.save()
    return redirect(url_for('list_apiaries'))


if __name__ == '__main__':
    """Main function"""

    host = environ.get('APPIARY_API_HOST')
    port = environ.get('APPIARY_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5555'
    app.run(host=HOST, port=PORT, debug=True)

