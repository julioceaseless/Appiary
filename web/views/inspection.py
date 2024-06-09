#!/usr/bin/python3
"""Inspection routes"""

from models import storage
from web.views import views
from flask import render_template, request, redirect, url_for
from flask import session
from models.inspection import Inspection
from models.beehive import Beehive
from models.Apiary import Apiary


@views.route('/inspections')
def list_inspections():
    """List inspections"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('views.login'))

    # Query inspections directly related to the user's apiaries
    inspections = storage.query(Inspection).join(Beehive).join(Apiary).filter(Apiary.user_id == user_id).all()
    inspection_list = [inspection.id for inspection in inspections]
    inspection_list.sort()

    return render_template('list_inspections.html', inspections=inspection_list)

@views.route('/inspection/<inspection_id>')
def view_inspection(inspection):
    """View inspection details"""
    inspection = storage.get('Inspection', inspection_id)

    return render_template('view_inspection.html', inspection=inspection)

@views.route('/inspection/add', methods=['GET', 'POST'])
def add_inspection():
    """Add new inspection"""
    if request.method == 'POST':
        hive_id= request.form.get('hive_id')
        notes = request.form.get('notes')
        status = request.form.get('status')

        data = {'hive_id': hive_id,
                'observations': notes,
                'ready_for_harvest': status
                }
        inspection = Inspection(**data)
        inspection.save()
        return redirect(url_for('views.list_inspections'))

    hives = storage.query(Beehive).join(Apiary).filter(Apiary.user_id == user_id).all()
    hive_list = [hive.id for hive in hives]
    return render_template('add_inspection.html', hives=hive_list)

@views.route('/inspection/delete/<inspection_id>', methods=['GET'])
def delete_inspection(inspection_id):
    """Delete inspection"""
    inspection = storage.get('Inspection', inspection_id)
    storage.delete(inspection)
    storage.save()
    return redirect(url_for('views.list_inspections'))
