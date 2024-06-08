#!/usr/bin/python3
"""Authentication endpoints"""

from models import storage
from models.user import User
from web.views import views
from os import environ
from flask import render_template, url_for, request, redirect


@views.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        yob = request.form.get('yob')

        data = {'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'yob': yob
            }
        user = User(**data)
        user.save()
        return redirect(url_for('views.show_profile', user_data=user.view_profile()))
    return render_template("sign-up.html")


@views.route("/profile")
def show_profile(user_data):
    return user_data

