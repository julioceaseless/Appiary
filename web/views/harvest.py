#!/usr/bin/python3
"""Inspection routes"""

from models import storage
from web.views import views
from flask import render_template, request, redirect, url_for
from flask import session
from decorators import login_required
from models.harvest import Harvest
from models.beehive import Beehive
from models.apiary import Apiary


@views.route('/harvests')
@login_required
def list_harvests(user_id):
    """List all the harvests performed"""

    # Query harvests directly related to the user's apiaries
    harvests = storage.query(Harvest).join(Beehive).join(Apiary).filter(Apiary.user_id == user_id).all()
    harvest_list = [harvest.id for harvest in harvests]

    return render_template('list_harvests.html', harvests=harvest_list,
                                                    size=len(harvest_list))

@views.route('/harvest/<harvest_id>')
@login_required
def view_harvest(user_id, harvest_id):
    """View harvest details"""
    harvest = storage.get('Harvest', harvest_id)

    return render_template('view_harvest.html', harvest=harvest)

@views.route('/harvest/add', methods=['GET', 'POST'])
@login_required
def add_harvest(user_id):
    """Add new harvest event"""
    if request.method == 'POST':
        hive_id = request.form.get('hive_id')
        notes = request.form.get('notes')
        quantity = float(request.form.get('quantity'))

        data = {'hive_id': hive_id,
                'notes': notes,
                'quantity': quantity
                }
        harvest = Harvest(**data)
        harvest.save()

        # schedule the next tentative harvest date
        harvest.set_next_harvest()

        return redirect(url_for('views.list_harvests'))
    
    ready_hives = []

    #retrieve all hives for user
    hives = (
            storage.query(Beehive)
            .join(Apiary)
            .filter(Apiary.user_id == user_id)
            .all()
            )
    
    # filter ready hives
    for hive in hives:
        if hive.ready_for_harvest:
            ready_hives.append(hive)

    return render_template('add_harvest.html', hives=ready_hives)

@views.route('/harvest/delete/<harvest_id>', methods=['GET'])
@login_required
def delete_harvest(user_id, harvest_id):
    """Delete harvest"""
    harvest = storage.get('Harvest', harvest_id)
    storage.delete(harvest)
    storage.save()
    return redirect(url_for('views.list_harvests'))
