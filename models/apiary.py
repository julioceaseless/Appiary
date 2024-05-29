#!/usr/bin/python3
""" Create an Apiary"""
import models
from models.base_model import BaseModel, Base
from os import environ
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Apiary(BaseModel, Base):
    """define an apiary"""
    if models.storage_type == 'db':
        __tablename__ = 'apiaries'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(60), nullable=False)
        longitude = Column(Float, nullable=True)
        latitude = Column(Float, nullable=True)
        description = Column(String(1024), nullable=True)

        # Establish relationship with Beehive
        beehives = relationship('Beehive', backref='apiary',
                                cascade='all, delete-orphan')
    else:
        user_id = ""
        name = ""
        longitude = ""
        latitude = ""
        description = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
