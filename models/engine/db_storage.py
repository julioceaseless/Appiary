#!/usr/bin/python3
"""
Database storage engine
"""

from models.base_model import BaseModel, Base
from models.apiary import Apiary
from models.user import User
from models.beehive import Beehive
from models.inspection import Inspection
from models.harvest import Harvest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
from os import environ


all_classes = {'Apiary': Apiary, 'User': User,
               'Beehive': Beehive, 'Inspection': Inspection,
               'Harvest': Harvest
               }


class DBStorage:
    """
    This is a class to manage MSQL storage using SQLAlchemy
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        create SQLAlchemy engine
        """

        # create engine
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".
                                      format(environ.get('APPIARY_MYSQL_USER'),
                                             environ.get('APPIARY_MYSQL_PWD'),
                                             environ.get('APPIARY_MYSQL_HOST'),
                                             environ.get('APPIARY_MYSQL_DB')),
                                      pool_pre_ping=True)

        # drop tables
        if environ.get('APPIARY_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session
        Return: dictionary (<class-name>.<object-id>: <obj>)
        """
        obj_dict = {}

        if cls:
            cls_obj = all_classes.get(cls)
            objs = self.__session.query(cls_obj).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
        else:
            for val in all_classes.values():
                for obj in self.__session.query(val):
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """
        Add object to current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete obj from database session
        """
        if obj:
            # determine class from obj
            cls_name = all_classes[type(obj).__name__]

            # query class table and delete
            self.__session.query(cls_name).\
                filter(cls_name.id == obj.id).delete()

    def reload(self):
        """
        Create database session
        """
        # create session from current engine
        Base.metadata.create_all(self.__engine)
        # create db tables
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        # previousy:
        # Session = scoped_session(session)
        self.__session = scoped_session(session)

    def query(self, cls):
        """
        Query all objects of a given class
        """
        return self.__session().query(cls)

    def close(self):
        """
        Close scoped session
        """
        self.__session.remove()

    def get(self, cls, id):
        """ retrieves one object """
        # check if cls is valid and exists
        if cls and id:
            if isinstance(cls, str) and cls in all_classes.keys():
                cls_obj = all_classes[cls]
            else:
                cls_obj = cls
            # search in current database session
            try:
                obj = self.__session.query(cls_obj).get(id)
                return obj
            except Exception as e:
                return None
        else:
            return None

    def count(self, cls=None):
        """count the number of records"""
        if cls:
            return len(self.all(cls))
        else:
            return len(self.all())
