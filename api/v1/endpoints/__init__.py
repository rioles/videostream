#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.endpoints.user.user_role import *
from api.v1.endpoints.user.user_permission import *
from api.v1.endpoints.user.role_permission import *
from api.v1.endpoints.user.user_auth import *


