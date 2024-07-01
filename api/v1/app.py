from flask import Flask, make_response, jsonify, redirect, request
from services.user_services.user_crud import ObjectManager
from flask_cors import CORS
from models.user import User
from models import storage
from api.v1.endpoints import app_views
import os
import secrets

from os import getenv

from flask_login import LoginManager
login_manager = LoginManager()


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
login_manager.init_app(app)
cors = CORS(app, resources={r"api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

@login_manager.unauthorized_handler
def unauthorized():
    base = request.base_url
    base_arr = base.split("/")
    base_correct = "/".join(base_arr[:-1])
    url = f"{base_correct}/user_auth"
    return redirect(url)

@login_manager.user_loader
def loader_user(user_id):
    obj = ObjectManager()
    user = obj.find_object_by(User, **{'id':user_id})
    return user

@app.teardown_appcontext
def teardown(self):
    """ Calls storage close"""
    storage.close()


@app.errorhandler(404)
def pageNotFound(error):
    """Error handling for 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('AUT_API_HOST', default='0.0.0.0')
    port = getenv('AUT_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)