#!/usr/bin/python3
'''Start a flask web application'''
from models import storage
from web.views import views
from os import environ
from flask import Flask, render_template, request, redirect, url_for


# start flask
app = Flask(__name__)

# register blueprints
app.register_blueprint(views)

@app.teardown_appcontext
def close_db(error):
    """close the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    """Main function"""

    HOST = environ.get('APPIARY_API_HOST')
    PORT = environ.get('APPIARY_API_PORT')
    if not HOST:
        HOST = '0.0.0.0'
    if not PORT:
        PORT = '5555'
    app.run(host=HOST, port=PORT, debug=True)
