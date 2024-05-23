#!/usr/bin/python3
'''
This is a parent model
'''
import uuid
from datetime import datetime


time = "%Y-%m-%dT%H:%M:%S.%f"
class BaseModel:
    """This is the base model"""
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
        obj_to_dict = self.__dict__.copy()
        # add class attribute
        obj_to_dict['__class__'] = self.__class__.__name__
        # convert datetime object to ISO formart
        obj_to_dict['created_at'] = self.created_at.isoformat()
        obj_to_dict['updated_at'] = self.updated_at.isoformat()
        return obj_to_dict


    def __str__(self):
        """Return String representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.to_dict())

    
    def update(self):
        """save and update 'updated_at' the time to current time"""
        self.updated_at = datetime.utcnow()
