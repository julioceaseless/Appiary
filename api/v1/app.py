#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from app.v1.auth import api_auth
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flasgger import Swagger
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

# Determine the absolute path to swagger.yaml
swagger_yaml_path = os.path.join(os.path.dirname(__file__), '../../docs/swagger.yaml')

# integrate swagger to flask app and point it to swagger.yaml file
swagger = Swagger(app, template_file=swagger_yaml_path)

# register blueprints
app.register_blueprint(app_views)
app.register_blueprint(api_auth)

# handle cross-origin requests errors between js and python
# cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    404 Error
    ---
    responses:
      404:
        description: Resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    HOST = environ.get('APPIARY_API_HOST')
    PORT = environ.get('APPIARY_API_PORT')
    DEBUG = environ.get('DEBUG_FLAG')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=DEBUG_FLAG)
