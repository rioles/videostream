from dataclasses import dataclass, field
from models.role import Role
from models.user import User
from models.permission import Permission
@dataclass
class UserRoleEntity:
    role: Role
    user: User
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        my_dict["role"] = self.role.to_dict()
        my_dict["user"] = self.user.to_dict()
        if "_sa_instance_state" in my_dict:
            del my_dict["_sa_instance_state"]
        return my_dict
    

