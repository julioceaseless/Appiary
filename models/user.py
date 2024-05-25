#!/usr/bin/python3
"""User model"""
import models
from models.base_model import BaseModel, Base
from os import environ
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

class User(BaseModel, Base):
    """
    create user class
    """
    if models.storage_type == 'db':
        __tablename__ = 'users'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        yob = Column(Integer, nullable=False)

    else:
        first_name = ""
        last_name = ""
        email = ""
        yob = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    if models.storage_type != 'db':
        @property
        def age(self):
            """create age property from yob and current year"""
            current_year = datetime.now().year
            if self.yob > 0 and (current_year - self.yob) > 1:
                return current_year - self.yob
            else:
                return 0

    def view_profile(self):
        """show user information"""
        user_info = {}
        for key, value in self.__dict__.items():
            if key not in ['id', 'updated_at', '__class__']:
                if key == "created_at":
                    user_info["Joined"] = f'{value.strftime("%B")}, {value.year}'
                    continue
                user_info[key] = value
        user_info['age'] = self.age
        return user_info
