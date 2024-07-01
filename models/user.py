#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Boolean
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    __tablename__ = 'user'
    username = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    name = Column(String(128),  nullable=False)
    user_givename = Column(String(128),  nullable=False)
    profil_picture = Column(String(128), nullable=False)
    email_verified = Column(Boolean, default=True, nullable=True)
    roles = relationship('Role', secondary='user_role', back_populates="users")

    
