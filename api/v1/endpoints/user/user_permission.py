from math import ceil
from services.user_services.user_crud import ObjectManager
from api.v1.endpoints import app_views
from flask import abort, jsonify, make_response, request
from services.user_services.paginator import Paginator
from models.permission import Permission

obj = ObjectManager()
permissions = obj.find_all(Permission)
page_obj = Paginator(permissions)
print(page_obj.get_page())


@app_views.route('/permission', methods=['POST'], strict_slashes=False)
def post_permission():
    """create a new role"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    permission_register = ObjectManager()
    permission = permission_register.add_object(
        Permission, **request.get_json())
    return make_response(jsonify(permission.to_dict()), 201)

@app_views.route('/permission/<string:permission_id>', methods=['PUT'], strict_slashes=False)
def update_permission(permission_id):
    """update a  role"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    permission_register = ObjectManager()
    permission_register.update_object_in_storage(Permission, permission_id, **request.get_json())
    return make_response(jsonify({'status': '201', 'message': 'update make'}), 201)

@app_views.route('/permission/<string:permission_id>', methods=['GET'], strict_slashes=False)
def get_permission(permission_id):
    """update a  role"""
    criteria = {"id": permission_id}
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    permission = obj.find_object_by(Permission, **criteria)
    return make_response(jsonify(permission.to_dict()), 201)



@app_views.route('/permission/<string:permission_name>', methods=['GET'], strict_slashes=False)
def get_permission_by_name(permission_name):
    """update a  role"""
    criteria = {"name": permission_name}
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    permission = obj.find_object_by(Permission, **criteria)
    return make_response(jsonify(permission.to_dict()), 201)




@app_views.route('/permission/<string:permission_id>', methods=['GET'], strict_slashes=False)
def delete_permission(permission_id):
    """update a  role"""
    criteria = {"id": permission_id}
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    permission = obj.delete_object(Permission, **criteria)
    return make_response(jsonify(permission.to_dict()), 201)

@app_views.route('/permissions', methods=['GET'], strict_slashes=False)
def get_permissions():
    """get permission informations"""
    obj = ObjectManager()
    permissions = obj.find_all(Permission)
    page_obj = Paginator(permissions)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)

 