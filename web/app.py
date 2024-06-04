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
    # show stats in dashboard
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

@app.route('/beehives')
def list_beehives():
    """List beehives"""
    beehive_list = []
    all_hives = storage.all('Beehive')
    for hive in all_hives.values():
        beehive_list.append(hive.id)
    return render_template('list_beehives.html', beehives=beehive_list,
                                                 size=len(beehive_list))

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

@app.route('/beehive/<beehive_id>')
def view_beehive(beehive_id):
    """View beehive"""
    beehive = storage.get('Beehive', beehive_id)
    return render_template('view_beehive.html', beehive=beehive)

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

@app.route('/beehive/add', methods=['GET', 'POST'])
def add_beehive():
    """Add new beehive"""
    if request.method == 'POST':
        apiary_id = request.form['apiary']
        data = {'apiary_id': apiary_id}
        beehive = Beehive(**data)
        beehive.save()
        return redirect(url_for('list_beehives'))

    apiaries = storage.all('Apiary')
    return render_template('add_beehive.html', apiaries=apiaries)

@app.route('/apiary/delete/<apiary_id>', methods=['GET'])
def delete_apiary(apiary_id):
    """Delete apiary"""
    apiary = storage.get('Apiary', apiary_id)
    storage.delete(apiary)
    storage.save()
    return redirect(url_for('list_apiaries'))

@app.route('/beehive/delete/<beehive_id>', methods=['GET'])
def delete_beehive(beehive_id):
    """Delete apiary"""
    beehive = storage.get('Beehive', beehive_id)
    storage.delete(beehive)
    storage.save()
    return redirect(url_for('list_beehives'))


if __name__ == '__main__':
    """Main function"""

    HOST = environ.get('APPIARY_API_HOST')
    PORT = environ.get('APPIARY_API_PORT')
    if not HOST:
        HOST = '0.0.0.0'
    if not PORT:
        PORT = '5555'
    app.run(host=HOST, port=PORT, debug=True)

