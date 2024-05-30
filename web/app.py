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
    return render_template('index.html')

@app.route('/apiaries')
def list_apiaries():
    apiary_list = []
    apiaries = storage.all('Apiary')
    for key in apiaries.keys():
        apiary_list.append(key.replace('.',': '))
    return render_template('list_apiaries.html', apiaries=apiary_list)

@app.route('/apiary/<apiary_id>')
def view_apiary(apiary_id):
    apiary = storage.get('Apiary', apiary_id)
    return render_template('view_apiary.html', apiary=apiary)

@app.route('/apiary/add', methods=['GET', 'POST'])
def add_apiary():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['latitude']
        new_apiary = Apiary(name=name, latitude=latitude)
        new_apiary.save()
        return redirect(url_for('list_apiaries'))
    return render_template('add_apiary.html')

@app.route('/apiary/delete/<int:apiary_id>', methods=['POST'])
def delete_apiary(apiary_id):
    apiary = Apiary.query.get_or_404(apiary_id)
    db.session.delete(apiary)
    db.session.commit()
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

