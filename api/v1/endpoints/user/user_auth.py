import json
from typing import Optional,Any, Type, Dict
import os
from math import ceil
from typing import Any, Dict
from flask_cors import cross_origin
import uuid
from flask import session
from domain.user.user_role import UserRoleEntity
from dto.auth_config_dto import GoogleOAuthConfig
from dto.type_of_service import service_dict
from models.role import Role
from models.user import User
from models.user_role import UserRoles
from repository.auth_service import AoutService
from services.user_services.auth_service_factory import AuthServiceFactory
from services.user_services.google_auth_const import GoogleOAuthConstants
from services.user_services.user_crud import ObjectManager
from api.v1.endpoints import app_views
from flask import abort, jsonify, make_response, request
from services.user_services.paginator import Paginator
from models.permission import Permission
from flask import Flask, redirect,current_app
#from services.user_services.google_aout import 
from oauthlib.oauth2 import WebApplicationClient
from services.user_services.process_user_info import UserDataProcessor
from flask_login import (
    login_required,
    logout_user,
    current_user,
    login_user
)


client_code = os.environ.get('GOOGLE_CLIENT_SECRET') 
client_id= os.environ.get('GOOGLE_CLIENT_ID')
url = os.environ.get('GOOGLE_DISCOVERY_URL')
my_config: GoogleOAuthConfig.Builder = GoogleOAuthConfig.Builder()
config = my_config.client_id(client_id).client_secret(client_code).discovery_url(GoogleOAuthConstants.get_discovery_url()).redirect_url(GoogleOAuthConstants.get_redirect_uri()).build()

service_type = "google_auth"
auth_object: AoutService = AuthServiceFactory.create_service(service_type, config, service_dict)

obj_manager:ObjectManager = ObjectManager()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
@cross_origin()
@app_views.route('/after_log', methods=['GET', 'POST'], strict_slashes=False)
def logged_user():
    user_role = session.get('user_role')
    oauth2_token = session.get('oauth2_token')
    return  make_response(jsonify({"user_email":current_user.email,"profil_picture":current_user.profil_picture, "oauth2_token":oauth2_token, "role":user_role, "name":current_user.name}), 201)
    
@cross_origin()
@app_views.route('/user_auth', methods=['GET', 'POST'], strict_slashes=False)
def auth_user():
    url: str = ""
    role = {'role':request.get_json()['role']}
    user_data_processor:UserDataProcessor = UserDataProcessor.Builder()\
    .build()
    url = user_data_processor.generate_login_uri("user_login",role,"role" )
    return redirect(url)
  
@cross_origin()
@app_views.route('/user_login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    role = request.args.get('role')
    request_uri = auth_object.get_uri(role)
    return redirect(request_uri)

@cross_origin()
@app_views.route('/login/callback/google', methods=['GET','POST'], strict_slashes=False)
def aout_callbac():
    code = request.args.get('code')
    state = request.args.get("state")
    role = decode_get_role(state)
    
    processor = UserDataProcessor.Builder().build()
    bases = processor.generate_login_uri("after_log")
    

    oauth2_token = auth_object.get_access_token(code)
    
    user_data_processor = UserDataProcessor.Builder()\
        .obj(obj_manager)\
        .auth_object(auth_object)\
        .code(code)\
        .redirect_url(bases)\
        .build()

    user_data = user_data_processor.extract_user_info(oauth2_token)
    role_data = {'name':role['role']}

    obj = ObjectManager()
    user: User = obj.find_object_by(User, **{'id': user_data['id']})
    roles: Role = obj.find_object_by(Role, **role_data)
    
    if user is  None:
        user = obj.add_object(
        User, **user_data)
        
    processor = UserDataProcessor.Builder()\
        .auth_object(auth_object)\
        .user(user)\
        .obj(obj)\
        .build()

    result = processor.process_user_data(oauth2_token,role, roles, current_user, login_user, role_data, bases)
    login_user(user)
    return redirect(result) if result else redirect(bases)
    
@cross_origin()
@app_views.route('/logout/', methods=['GET','POST'], strict_slashes=False)
def logout():
    logout_user()
    request_uri = "/index"
    return redirect(request_uri)

@cross_origin()
@app_views.route('/logout/', methods=['GET','POST'], strict_slashes=False)
def index():
    return f'<p> please login</p>'
    

def generatestte(parameter:str):
    uuid_str = str(uuid.uuid4())
    parameter_with_uuid = f"{uuid_str}.{parameter}"
    data = {
            "role": parameter_with_uuid
        }
    return json.dumps(data)

def decode_get_role(output_str:str):
    full_dict = json.loads(output_str)
    role_value = full_dict.get("role", "")
    _, role_str = role_value.split('.')
    return {"role":role_str}

