from typing import Optional

class UserDataProcessor:
    def __init__(self, oauth2_token: str, user_data: dict, obj, role, roles, role_data: dict, bases: str, user):
        self.oauth2_token = oauth2_token
        self.user_data = user_data
        self.obj = obj
        self.role = role
        self.roles = roles
        self.role_data = role_data
        self.bases = bases
        self.user = user

    def process_user_data(self) -> Optional[str]:
        """
        Process user data and perform role-related actions based on the provided data.

        Returns:
            str: A string containing a base URL or redirect destination, or None if no explicit return is found.
        """
        if self.roles is not None:
            pot_user_role = self.obj.find_object_by(UserRoles, **{'user_id': self.user_data['id'], 'role_id': self.roles.id})
            if pot_user_role is not None:
                obj = {'status': '409', 'message': f"this user has already {self.role['role']} role"}
                print(obj)
                print(current_user.is_authenticated)
                if not current_user.is_authenticated:
                    login_user(self.user)
                # login_user(self.user)
                session['user_role'] = self.role['role']
                session['oauth2_token'] = self.oauth2_token
                return self.bases
            else:
                user_role_data = {'user_id': self.user.id, 'role_id': self.roles.id}
                user_role = self.obj.add_object(UserRoles, **user_role_data)
                return None
        else:
            roles = self.obj.add_object(Role, **self.role_data)
            user_role_data = {'user_id': self.user.id, 'role_id': roles.id}
            user_role = self.obj.add_object(UserRoles, **user_role_data)

        return None


