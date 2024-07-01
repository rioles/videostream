import json
from typing import Any, Dict, Optional, Union
from models.user import User
from models.role import Role
from flask import session
from models.user_role import UserRoles
from repository.auth_service import AoutService
from services.user_services.user_crud import ObjectManager
from flask import request
import uuid


class UserDataProcessor:
    def __init__(self, builder):
        self.__obj = builder._Builder__obj
        self.__auth_object = builder._Builder__auth_object
        self.__code = builder._Builder__code
        self.__redirect_url = builder._Builder__redirect_url
        self.__response_json = builder._Builder__response_json
        self.__user = builder._Builder__user

    @property
    def obj(self):
        return self.__obj

    @property
    def auth_object(self):
        return self.__auth_object

    @property
    def code(self):
        return self.__code

    @property
    def redirect_url(self):
        return self.__redirect_url

    @property
    def response_json(self):
        return self.__response_json

    @property
    def user(self):
        return self.__user

    class Builder:
        def __init__(self):
            self.__obj = None
            self.__auth_object = None
            self.__code = None
            self.__redirect_url = None
            self.__response_json = None
            self.__user = None

        def obj(self, obj):
            self.__obj = obj
            return self

        def auth_object(self, auth_object):
            self.__auth_object = auth_object
            return self

        def code(self, code):
            self.__code = code
            return self

        def redirect_url(self, redirect_url):
            self.__redirect_url = redirect_url
            return self

        def response_json(self, response_json):
            self.__response_json = response_json
            return self

        def user(self, user):
            self.__user = user
            return self

        def build(self):
            return UserDataProcessor(self)

    def generate_login_uri(self,endpoint: str, parameter: Optional[Union[str, Dict[str, Any]]] = None, parameter_name:Optional[str] = None) -> str:
        """
        Generate a login URI with an optional  query parameter.

        Args:
            parameter (str, optional): The parameter to be included as a query parameter.

        Returns:
            str: The generated URI.
        """
        base = request.base_url
        base_correct = '/'.join(base.split('/')[0:5])
        #print("this is base_urlll", base_correct)
        base_corrects = "https://d9b2-156-0-214-24.ngrok-free.app/api/v1"
        #print("this is basess urriiii", '/'.join(base_corrects.split('/')[0:5]))
        if parameter:
            url = f"{base_correct}/{endpoint}?{parameter_name}={parameter}"
            print("this is url:",url)
        else:
            url = f"{base_corrects}/{endpoint}"

        return url
    
    def generate_parameter(self, parameter:str):
        uuid_str = str(uuid.uuid4())
        parameter_with_uuid = f"{uuid_str}.{parameter}"
        data = {
                "role": parameter_with_uuid
            }
        return json.dumps(data)
    
    def extract_user_info(self, token) -> Dict[str, str]:
        """
        Extract user information from a JSON response.

        Args:
            response_json (dict): The JSON response containing user information.

        Returns:
            dict: A dictionary containing user information with the following keys:
                - 'email': User's email address (str)
                - 'profile_picture': URL to the user's profile picture (str)
                - 'id': User's unique identifier (str)
                - 'username': User's username (str)

        Example:
            response_json = {
                'email': 'user@example.com',
                'picture': 'https://example.com/profile.jpg',
                'sub': '123456789',
                'email_verified': True
            }

            user_data = extract_user_info(response_json)
            print(user_data)
        """
        response_json = self.auth_object.get_user_info(token)
        print("user innfggf2", response_json)
        user_info = {
            'email': response_json.get('email', ''),
            'profil_picture': response_json.get('picture', ''),
            'id': response_json.get('sub', ''),
            'user_givename': response_json.get('family_name', ''),
            'name': response_json.get('given_name', ''),
            'email_verified': response_json.get('email_verified', ''),
            'username': response_json.get('email', ''),
        }
        return user_info
    
    
    def process_user_data(self, token, role, roles:Role, current_user, login_user, role_data: dict, bases)->Optional[str]:
        
        """
        Process user data and perform role-related actions based on the provided data.

        Args:
            user_data (dict): User information dictionary.
            obj: Your database or object management utility.
            roles: Existing roles object (if roles are not None).
            role_data (dict): Data for creating a new role if roles are None.
            bases: Base URL or redirect destination.

        Returns:
            flask.Response: A response object, or None if no explicit return is found.

        Example:
            user_data = {
                'id': '123456789',
                'email': 'user@example.com',
                'profile_picture': 'https://example.com/profile.jpg',
                # Other user data...
            }

            # Define obj, roles, role_data, and bases as needed.

            response = process_user_data(user_data, obj, roles, role_data, bases)
        """
        user_data = self.extract_user_info(token)
        print("this is user data", user_data)
       
        if roles is not None:
            pot_user_role = self.obj.find_object_by(UserRoles, **{'user_id': user_data['id'], 'role_id': roles.id})
            if pot_user_role is not None:
                obj = {'status': '409', 'message': f"this user has already {role['role']} role"}
                print(obj)
                print(current_user.is_authenticated)
                if not current_user.is_authenticated:
                    login_user(self.user)
                # login_user(user)
                session['user_role'] = role['role']
                
                return bases
            else:
                user_role_data = {'user_id': self.user.id, 'role_id': roles.id}
                user_role = self.obj.add_object(UserRoles, **user_role_data)
                session['user_role'] = role['role']
                
                return None
        else:
            roles = self.obj.add_object(Role, **role_data)
            user_role_data = {'user_id': self.user.id, 'role_id': roles.id}
            session['user_role'] = role['role']
            #session['oauth2_token'] = oauth2_token
            user_role = self.obj.add_object(UserRoles, **user_role_data)     
        return None
    

 # Output: some_code


