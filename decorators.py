#!/usr/bin/python3
"""Appiary/decorators.py """
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in to access this page.")
            return redirect(url_for('views.login'))
        return f(user_id, *args, **kwargs)
    return decorated_function
