#!/usr/bin/env python3
import os
from sqlalchemy import Column, String, DateTime,func, create_engine, Numeric, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from typing import Any, Dict, Optional, TypeVar
from sqlalchemy.orm.exc import NoResultFound
from repository.auth_repository_interface import AuthRepo
from models.basic_base import Base
from models.base import BaseModel
from models.permission import Permission
from models.role import Role
from models.user import User
from models.user_role import UserRoles
from models.role_permission import RolePermissions
from dotenv import load_dotenv
load_dotenv()
T = TypeVar('T')
class DBSManager(AuthRepo):
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                            format(os.environ.get('VID_STREAM_DB'),
                                                   os.environ.get('PASSWORD'),
                                                   'localhost',
                                                   os.environ.get('DB'),                                                   
                                                   ), echo=True)
  
    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def new(self, obj)-> None :
        """add object to current session
        """
        self.__session.add(obj)

    def save(self):
        """commit current done work
        """
        self.__session.commit()

    def find_by(self, target_class: T,  **kwargs) -> Optional[T]:
        """
        Find a object by the given criteria
        Args:
            **kwargs: The criteria to search for
        Returns:
            T: The found object_t
        """

        try:
            object_t = self.__session.query(target_class).filter_by(**kwargs).first()
            if not object_t:
                raise NoResultFound("No object found")
            return object_t
        except NoResultFound:
            return None


    def find_all_by(self, target_class: T,  **kwargs) -> T:
        """
        Find a object by the given criteria
        Args:
            **kwargs: The criteria to search for
        Returns:
            T: The found object_t
        """

        try:
            object_t = self.__session.query(target_class).filter_by(**kwargs).all()
            if not object_t:
                raise NoResultFound("No object found")
            return object_t
        except NoResultFound:
            return []



    def get_sum_with_filter(
        self, 
        target_class: T,
        sum_param1: str,
        sum_param2: str = None,
        **kwargs:Dict[str, Any]
        ):
        
        """
        Calculate the sum based on the provided sum parameters and filter conditions.
    
        Args:
            target_class (type): The class representing the database table.
            sum_param1 (str, required): The first sum parameter attribute name.
            sum_param2 (str, optional): The second sum parameter attribute name. Defaults to None.
            **kwargs: Additional filter conditions as keyword arguments.

        Returns:
            int: The calculated sum based on the sum parameters and filter conditions.
        """
        
        if not hasattr(target_class, sum_param1) and not hasattr(target_class, sum_param2):
            raise AttributeError(f"{target_class.__name__} does not have attribute '{sum_param1}' or '{sum_param2}'.")
    
        if sum_param2 and not hasattr(target_class, sum_param2):
            raise AttributeError(f"{target_class.__name__} does not have attribute '{sum_param2}'.")
        if sum_param2:
            total_sum = self.__session.query(func.sum(getattr(target_class, sum_param1) * getattr(target_class, sum_param2))).filter_by(**kwargs).scalar()
        else:
            total_sum = self.__session.query(func.sum(getattr(target_class, sum_param1))).filter_by(**kwargs).scalar()
        return total_sum
    
    def update_object(self, target_class: T, value : str, **kwargs) -> None:
        """
        Update the given object
        Args:
            value (string): The id or another attribut of the class to update
            **kwargs: The fields to update
            target_class: the class over the update is made

        Returns:
            None
        """
        try:
            current_object = self.find_by(target_class, id = value)
            for key, value in kwargs.items():
                if hasattr(current_object, key):
                    setattr(current_object, key, value)
                else:
                    raise ValueError(f"{target_class.__name__} does not have attribute {key}")
            self.__session.commit()
        except (NoResultFound, ValueError):
            raise NoResultFound(f"No {target_class.__name__} found with id {id}")

    def get_all(self, target_class: T) -> T:
        """query on the current database session"""
        #session.query(Patient).filter(Patient.is_deleted == False).all()
        objs = self.__session.query(target_class).filter(target_class.is_deleted == False).all()
        return objs


    def delete(self, target_obj: T):
        """delete from the current database session obj if not None
        Args
            target_object (current_object type): object that is implied in delete operation
        Return
            None if object is None else current_object
        """
        if target_obj is not None:
            self.__session.delete(target_obj)


    def close(self)-> None :
        """call remove() method on the private session attribute"""
        self.__session.remove()
  
    
