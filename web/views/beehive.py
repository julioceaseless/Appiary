#!/usr/bin/python3
"""Beehive endpoints"""
from models import storage
from web.views import views
from os import environ
from flask import render_template, request, redirect, url_for
from flask import session
from models.beehive import Beehive


@views.route('/beehives')
def list_beehives():
    """List beehives"""
    beehive_list = []
    all_hives = storage.all('Beehive')
    print(session)
    for hive in all_hives.values():
        if hive.apiary.user_id == session.get('user_id'):
            beehive_list.append(hive.id)
    return render_template('list_beehives.html', beehives=beehive_list,
                                                 size=len(beehive_list))

@views.route('/beehive/<beehive_id>')
def view_beehive(beehive_id):
    """View beehive"""
    beehive = storage.get('Beehive', beehive_id)
    return render_template('view_beehive.html', beehive=beehive)

@views.route('/beehive/add', methods=['GET', 'POST'])
def add_beehive():
    """Add new beehive"""
    if request.method == 'POST':
        apiary_id = request.form['apiary']
        hive_type = request.form['type']
        wood_type = request.form['wood']
        data = {'apiary_id': apiary_id,
                'hive_type': hive_type,
                'wood_type': wood_type
               }
        beehive = Beehive(**data)
        beehive.save()
        return redirect(url_for('views.list_beehives'))

    apiaries = storage.all('Apiary')
    return render_template('add_beehive.html', apiaries=apiaries)


@views.route('/beehive/delete/<beehive_id>', methods=['GET'])
def delete_beehive(beehive_id):
    """Delete apiary"""
    beehive = storage.get('Beehive', beehive_id)
    storage.delete(beehive)
    storage.save()
    return redirect(url_for('views.list_beehives'))


