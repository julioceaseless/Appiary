#!/usr/bin/python3
"""Appiary/decorators.py """
from functools import wraps
from flask import session, jsonify, redirect, url_for, flash, current_app, request
from models import storage
from models.user import User
import jwt


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in to access this page.")
            return redirect(url_for('views.login'))
        return f(user_id, *args, **kwargs)
    return decorated_function

 
# define a decorator to protect API endpoints with JWT tokens
def token_required(f):
    """
    Decorator to ensure a valid token is present in the request.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        secret_key = request.headers.get('Key')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token.split()[1], secret_key, algorithms=["HS256"])
            current_user = storage.query(User).filter_by(email=data['user']).first()
        except Exception as e:
            return jsonify({
                'message': 'Token is invalid!',
                'error': str(e)
                }), 403
        return f(current_user, *args, **kwargs)
    return decorated
