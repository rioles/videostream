from math import ceil
from services.user_services.user_crud import ObjectManager
from api.v1.endpoints import app_views
from flask import abort, jsonify, make_response, request
from services.user_services.paginator import Paginator
from models.role import Role



@app_views.route('/role', methods=['POST'], strict_slashes=False)
def post_roles():
    """create a new enterprise"""
    print(request.get_json())
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    role = obj.add_object(
        Role, **request.get_json())
    return make_response(jsonify(role.to_dict()), 201)



@app_views.route('/role/<string:role_id>', methods=['PUT'], strict_slashes=False)
def update_role(role_id):
    """update a  role"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    role_register = ObjectManager()
    role_register.update_object_in_storage(Role, role_id, **request.get_json())
    return make_response(jsonify({'status': '201', 'message': 'update make'}), 201)

@app_views.route('/role/<string:role_id>', methods=['GET'], strict_slashes=False)
def get_role(role_id):
    """update a  role"""
    criteria = {"id": role_id}
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    role = obj.find_object_by(Role, **criteria)
    return make_response(jsonify(role.to_dict()), 201)


@app_views.route('/role/<string:role_id>', methods=['GET'], strict_slashes=False)
def delete_role(role_id):
    """update a  role"""
    criteria = {"id": role_id}
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj = ObjectManager()
    role = obj.delete_object(Role, **criteria)
    return make_response(jsonify(role.to_dict()), 201)

@app_views.route('/roles', methods=['GET'], strict_slashes=False)
def get_roles():
    """get amenity information for all patients"""
    obj = ObjectManager()
    roles = obj.find_all(Role)
    page_obj = Paginator(roles)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)

 