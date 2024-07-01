from typing import List
from models.permission import Permission
from dataclasses import dataclass, field
from services.user_services.user_crud import ObjectManager
from domain.user.role_perm import RolePermissionEntity
from models.role import Role

from models.role_permission import RolePermissions   
@dataclass
class AllRolePermissionManager:
    """
    A dataclass representing a manager for handling role permissions.

    This class manages a list of role permissions and provides methods to retrieve and manipulate them.

    Attributes:
        role_permisions (List[RolePermissions]): A list of RolePermissions objects.
        
    Methods:
        get_role_perms(): Retrieve a list of RolePermissions objects.
        get_all_role_permission(): Retrieve a list of all role permissions as dictionaries.
    """
    role_permisions: List[RolePermissions] = field(default_factory=list)
    def __post_init__(self):
        """
        Initialize the manager and retrieve role permissions if the list is empty.
        """
        if not self.role_permisions:
            self.role_permisions = self.get_role_perms()
        
    def get_role_perms(self) -> List[RolePermissions]:
        """
        Retrieve a list of all role permissions as dictionaries.

        Returns:
            List[dict]: A list of dictionaries representing role permissions.
        """
        obj = ObjectManager()
        role_permisions = obj.get_all_object(RolePermissions)
        return role_permisions
    
    def get_all_role_permission(self):
        list_of_role_perm = []
        for obj in self.role_permisions:
            ob = ObjectManager()
            role = ob.find_object_by(Role, **{"id":obj.role_id})
            permision = ob.find_object_by(Permission, **{"id":obj.permission_id})
            role_permission = RolePermissionEntity(role, permision)
            list_of_role_perm.append(role_permission.to_dict())
        return list_of_role_perm
