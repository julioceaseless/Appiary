#!/usr/bin/python3
"""
API login endpoint.
Description: Uses basic auth (username and password)
"""
from models import storage
from models.user import User
from api.v1.auth import api_auth
from werkzeug.security import check_password_hash
from flask import jsonify, make_response, abort, request
from decorators import token_required
import datetime
import jwt


timedelta_30_mins = datetime.timedelta(minutes=30)
utc_now = datetime.datetime.utcnow()

@api_auth.route('/login', methods=['POST'])
def login():
    """
    Endpoint to authenticate a user and return a JWT token.
    
    Usage:
        curl -H "Content-Type: application/json" 
        -d '{"email":"email","password":"password"}' 
        -X POST http://localhost:5000/api/v1/login

    Returns:
        JSON: jwt toke if authentication successful
    """
    auth = request.authorization
    if not auth or not auth.email or not auth.password:
        return make_response('Could not verify', 401,
                            {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    # retrieve user
    user = storage.query(User).filter_by(email == auth.email).first()
    if user:
        # check if password is correct
        if check_password_hash(user.password, password):
            # generate token
            token = jwt.encode({
                'user': auth.username,
                'exp': utcnow() + timedelta_30_mins
                }, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({'token': token}, 200)
        else:
            abort(401, description="Password incorrect!"))
    else:
        abort(401, description="User not found!")
