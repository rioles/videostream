from dataclasses import dataclass, field
from models.role import Role
from models.permission import Permission
@dataclass
class RolePermissionEntity:
    role: Role
    permission: Permission
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        my_dict["role"] = self.role.to_dict()
        my_dict["permission"] = self.permission.to_dict()
        if "_sa_instance_state" in my_dict:
            del my_dict["_sa_instance_state"]
        return my_dict
    

