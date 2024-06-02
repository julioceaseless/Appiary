#!/usr/bin/python3
'''Start a flask web application'''
from models import storage
from os import environ
from flask import Flask, render_template, request, redirect, url_for
from models.apiary import Apiary
from models.beehive import Beehive

# start flask
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/apiaries')
def list_apiaries():
    """List apiaries"""
    apiary_list = []
    apiaries = storage.all('Apiary')
    for obj in apiaries.values():
        apiary_list.append(f'{obj.name} - {obj.id}')
    return render_template('list_apiaries.html', apiaries=apiary_list)

@app.route('/apiary/<apiary_id>')
def view_apiary(apiary_id):
    """View apiary"""
    apiary = storage.get('Apiary', apiary_id)
    return render_template('view_apiary.html', apiary=apiary)

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

@app.route('/apiary/delete/<apiary_id>', methods=['POST'])
def delete_apiary(apiary_id):
    """Delete apiary"""
    apiary = storage.get('Apiary', apiary_id)
    storage.delete(apiary)
    storage.save()
    return redirect(url_for('list_apiaries'))

if __name__ == '__main__':
    """Main function"""

    # get host
    if environ.get('HOST'):
        HOST = environ.get('HOST')
    else:
        HOST = '0.0.0.0'

    # get port
    if environ.get('PORT'):
        PORT = environ.get('PORT')
    else:
        PORT = 5555

    app.run(host=HOST, port=PORT, debug=True)

