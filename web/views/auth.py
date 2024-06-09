#!/usr/bin/python3
"""Authentication endpoints"""

from models import storage
from models.user import User
from web.views import views
from os import environ
from flask import render_template, url_for, request, redirect
from flask import session, flash


@views.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        yob = request.form.get('yob')

        if not first_name or not last_name or not email or not yob:
            flash("All fields are required!")
            return redirect(url_for('views.sign_up'))

        try:
            yob = int(yob)
        except ValueError:
            flash("Year of birth must be an integer!")
            return redirect(url_for('views.sign_up'))

        data = {'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'yob': yob
            }

        user = User(**data)
        user.save()

        session['user_id'] = user.id
        return redirect(url_for('views.show_profile'))

    return render_template("sign-up.html")


@views.route("/profile")
@login_required
def show_profile(user_id):
    """Show profile"""
    user = storage.get(User, user_id)
    if not user:
        return redirect(url_for('views.sign_up'))

    user_data = user.view_profile()
    return render_template("profile.html", user_data=user_data)


@views.route("/login", methods=['GET', 'POST'])
def login():
    """Login user"""
    if request.method == "POST":
        email = request.form.get('email')

        if not email:
            flash("Email is required!")
            return redirect(url_for('views.login'))

        # Optimized search for the user by email
        user = storage.query(User).filter_by(email=email).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('views.show_profile'))

        flash("Invalid email or user does not exist")
        return redirect(url_for('views.login'))

    return render_template("login.html")


@views.route("/logout")
@login_required
def logout(user_id):
    session.pop('user_id', None)
    return redirect(url_for('views.login'))
