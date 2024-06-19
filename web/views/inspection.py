#!/usr/bin/python3
"""Inspection routes"""

from models import storage
from web.views import views
from flask import render_template, request, redirect, url_for
from flask import session
from decorators import login_required
from models.inspection import Inspection
from models.beehive import Beehive
from models.apiary import Apiary


@views.route('/inspections')
@login_required
def list_inspections(user_id):
    """List inspections"""
    inspection_list = []
    # Query inspections directly related to the user's apiaries
    inspections = storage.query(Inspection).join(Beehive).join(Apiary).filter(Apiary.user_id == user_id).all()
    inspection_list = [inspection.id for inspection in inspections]

    return render_template('list_inspections.html', inspections=inspection_list,
                                                    size=len(inspection_list))

@views.route('/inspection/<inspection_id>')
@login_required
def view_inspection(user_id, inspection_id):
    """View inspection details"""
    inspection = storage.get('Inspection', inspection_id)

    return render_template('view_inspection.html', inspection=inspection)

@views.route('/inspection/add', methods=['GET', 'POST'])
@login_required
def add_inspection(user_id):
    """Add new inspection"""
    if request.method == 'POST':
        hive_id= request.form.get('hive_id')
        notes = request.form.get('notes')
        status = request.form.get('status')
        status = status.lower() == 'ready'

        data = {'hive_id': hive_id,
                'observations': notes,
                'ready_for_harvest': status
                }
        inspection = Inspection(**data)
        inspection.save()
        if status:
            inspection.set_harvest_ready()
            storage.save()
        return redirect(url_for('views.list_inspections'))
    
    status_options = ['Ready', 'Not Ready']
    hives = storage.query(Beehive).join(Apiary).filter(Apiary.user_id == user_id).all()
    return render_template('add_inspection.html', hives=hives, status_options=status_options)

@views.route('/inspection/delete/<inspection_id>', methods=['GET'])
@login_required
def delete_inspection(user_id, inspection_id):
    """Delete inspection"""
    inspection = storage.get('Inspection', inspection_id)
    storage.delete(inspection)
    storage.save()
    return redirect(url_for('views.list_inspections'))
