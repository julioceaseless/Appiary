#!/usr/bin/python3
"""
Database storage engine
"""

from models.base_model import BaseModel, Base
from models.apiary import Apiary
from models.beehive import Beehive
from models.harvest import Harvest
from models.inspection import Insepction
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
import environ


all_classes = {'Apiary': Apiary, 'Beehive': Beehive,
               'Harvest': Harvest, 'Inspection': Inspection
               'User': User,
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
        Query and return all objects by class/generally
        Return: dictionary (<class-name>.<object-id>: <obj>)
        """
        obj_dict = {}

        if cls:
            for row in self.__session.query(cls).all():
                # populate dict with objects from storage
                obj_dict.update({"{}.{}: {}".
                                format(type(row).__name__, row.id, row})
        else:
            for val in all_classes.values():
                for row in self.__session.query(val):
                    obj_dict.update({"{}.{}: {}".
                                    format(type(row).__name__, row.id,): row})
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

    def close(self):
        """
        Close scoped session
        """
        self.__session.remove()
