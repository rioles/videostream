from math import ceil
from services.user_services.user_crud import ObjectManager
from api.v1.endpoints import app_views
from flask import abort, jsonify, make_response, request
from services.user_services.paginator import Paginator
from models.role_permission import RolePermissions
from services.user_services.role_perm import AllRolePermissionManager


@app_views.route('/role_permission', methods=['POST'], strict_slashes=False)
def post_role_permission():
    """create a new role"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    role_perm = obj.add_object(
        RolePermissions, **request.get_json())
    return make_response(jsonify(role_perm.to_dict()), 201)


@app_views.route('/roles_perms', methods=['GET'], strict_slashes=False)
def get_roles_perms():
    """get amenity information for all patients"""
    obj = AllRolePermissionManager()
    all_role_perms = obj.get_all_role_permission()
    page_obj = Paginator(all_role_perms)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)