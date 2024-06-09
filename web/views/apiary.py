#!/usr/bin/python3
"""Apiary endpoints"""

from models import storage
from web.views import views
from os import environ
from flask import render_template, request, redirect, url_for
from flask import session
from models.apiary import Apiary


@views.route('/apiaries')
def list_apiaries():
    """List apiaries"""
    apiary_list = []
    apiaries = storage.all('Apiary')
    for apiary in apiaries.values():
        if apiary.user_id == session.get('user_id'):
            apiary_list.append(f'{apiary.name} - {apiary.id}')
    apiary_list.sort()
    return render_template('list_apiaries.html', apiaries=apiary_list)

@views.route('/apiary/<apiary_id>')
def view_apiary(apiary_id):
    """View an apiary"""
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

@views.route('/apiary/add', methods=['GET', 'POST'])
def add_apiary():
    """Add new apiary"""
    if request.method == 'POST':
        user_id = request.form.get('user')
        name = request.form.get('name')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        data = {'user_id': user_id,
                'name': name,
                'latitude': latitude,
                'longitude': longitude
                }
        apiary = Apiary(**data)
        apiary.save()
        return redirect(url_for('views.list_apiaries'))

    users = storage.all('User')
    return render_template('add_apiary.html', users=users)

@views.route('/apiary/delete/<apiary_id>', methods=['GET'])
def delete_apiary(apiary_id):
    """Delete apiary"""
    apiary = storage.get('Apiary', apiary_id)
    storage.delete(apiary)
    storage.save()
    return redirect(url_for('views.list_apiaries'))


