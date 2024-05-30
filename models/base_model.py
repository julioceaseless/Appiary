#!/usr/bin/python3
'''
This is a parent model
'''
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import environ


time = "%Y-%m-%dT%H:%M:%S.%f"

if environ.get("APPIARY_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """This is the base model"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=created_at)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            # create instance from json
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()

            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()

            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    
    def to_dict(self):
        """serialize an object to dictionary"""
        # retrieve dictionary representation of the object
        obj_dict = self.__dict__.copy()
        # add class attribute
        obj_dict['__class__'] = self.__class__.__name__
        # convert datetime object to ISO formart
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()

        # remove InstanceState object
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return obj__dict


    def delete(self):
        """
        delete the current instance from storage
        """
        models.storage.delete(self)


    def save(self):
        """
        save and update by updating 'updated_at' attribute to
        current time
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def update(self):
        """
        Update the updated_at attribute to reflect the last
        time  change was made
        """
        self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return String representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.to_dict())
