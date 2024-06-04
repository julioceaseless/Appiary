#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flasgger import Swagger
import os


app = Flask(__name__)


# Determine the absolute path to swagger.yaml
swagger_yaml_path = os.path.join(os.path.dirname(__file__), '../../docs/swagger.yaml')

# integrate swagger to flask app and point it to swagger.yaml file
swagger = Swagger(app, template_file=swagger_yaml_path)
app.register_blueprint(app_views)

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
    host = environ.get('APPIARY_API_HOST')
    port = environ.get('APPIARY_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
