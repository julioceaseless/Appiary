#!/usr/bin/python3
"""Authentication endpoints"""

from models import storage
from models.user import User
from web.views import views
from os import environ
from flask import render_template, url_for, request, redirect
from flask import session, flash
from decorators import login_required


@views.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """
    Handles sign up process.
    POST method handles sign up data in the signup form
    GET method displays the form for user to create account
    """
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        yob = request.form.get('yob')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check empty fields
        if (not first_name or
                not last_name or
                not email or
                not yob or
                not password1 or
                not password2):
            flash("All fields are required!", category="error")
            return redirect(url_for('views.sign_up'))

        # check if email exists
        email_exists = storage.query(User).filter_by(email=email).first()

        # catch errors
        if email_exists:
            flash("Email is already in use", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match!", category="error")
        elif len(password) < 5:
            flash("Password too short!", category="error")

        # calculate age
        try:
            yob = int(yob)
        except ValueError:
            flash("Year of birth must be an integer!")
            return redirect(url_for('views.sign_up'))

        data = {'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'yob': yob
            'password': password1
            }
        
        # create new user
        user = User(**data)
        user.save()

        # Set session id
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
        password = request.form.get('password')

        if not email or not password:
            flash("Password or Email is missing!")
            return redirect(url_for('views.login'))

        # Optimized search for the user by email
        user = storage.query(User).filter_by(email=email).first()
        if user:
            # check if password is correct
            if user.password == password:
                # set session id
                session['user_id'] = user.id
                # show login success notification
                flash("Logged in!", category="success")
                # show user profile
                return redirect(url_for('views.show_profile'))
            else:
                flash("Password incorrect!", category="error")
                return redirect(url_for('views.login'))
        
        flash("Invalid email or user does not exist", category="error")
        return redirect(url_for('views.login'))

    return render_template("login.html")


@views.route("/logout")
@login_required
def logout(user_id):
    session.pop('user_id', None)
    return redirect(url_for('views.login'))
