#!/usr/bin/python3
"""Apiary endpoints"""

from models import storage
from web.views import views
from os import environ
from flask import render_template, request, redirect, url_for
from flask import session
from models.apiary import Apiary
from decorators import login_required
import requests


def get_weather(api_key, obj):
    """Method retrieves weather data"""
    # create URL for API request to the WeatherMap
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    url_params = {
            "lat": obj.latitude,
            "lon": obj.longitude,
            "appid": api_key
            }

    # make GET request
    response = requests.get(base_url, url_params)

    # check if request is successfull
    if response.status_code == 200:
        # parse json
        data = response.json()
        return data
    else:
        data = {"Error": response.status_code}
        return data


@views.route('/apiaries')
@login_required
def list_apiaries(user_id):
    """List apiaries"""
    apiary_list = []
    apiaries = storage.query(Apiary).filter_by(user_id=user_id).all()
    for apiary in apiaries:
        apiary_list.append(f'{apiary.name} - {apiary.id}')
    apiary_list.sort()
    return render_template('list_apiaries.html', apiaries=apiary_list,
                                                 count=len(apiary_list))

@views.route('/apiary/<apiary_id>')
@login_required
def view_apiary(user_id, apiary_id):
    """View an apiary"""
    hive_count = 0
    weather_api_key = "abcb6b88edb80a24024ad742079ecdd9"

    apiary = storage.get('Apiary', apiary_id)

    # get weather data
    weather_data = get_weather(weather_api_key, apiary)
    
    weather = weather_data['weather'][0]['description'].capitalize()
    location = f"{weather_data['name']}, {weather_data['sys']['country']}"
    icon_code = weather_data['weather'][0]['icon']
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"

    print(weather_data)
    
    # check number of hives in apiary
    hives = storage.all('Beehive')
    if hives:
        for hive in hives.values():
            if hive.apiary_id == apiary_id:
                hive_count += 1

    # put everything in a dict
    data = {
            "apiary": apiary,
            "weather": weather,
            "location": location,
            "icon_url": icon_url,
            "hive_count": hive_count
            }

    return render_template('view_apiary.html', data=data)

@views.route('/apiary/add', methods=['GET', 'POST'])
@login_required
def add_apiary(user_id):
    """Add new apiary"""
    google_map_api_key = environ.get('GOOGLE_MAP_API')
    if request.method == 'POST':
        name = request.form.get('name')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        description = request.form.get('description')
        data = {'user_id': user_id,
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
                'description': description
                }
        apiary = Apiary(**data)
        apiary.save()
        return redirect(url_for('views.list_apiaries'))

    users = storage.all('User')
    return render_template('add_apiary.html', users=users,
                                              google_map_api_key=google_map_api_key)

@views.route('/apiary/delete/<apiary_id>', methods=['GET'])
@login_required
def delete_apiary(user_id, apiary_id):
    """Delete apiary"""
    apiary = storage.get('Apiary', apiary_id)
    storage.delete(apiary)
    storage.save()
    return redirect(url_for('views.list_apiaries'))
