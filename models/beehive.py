#!/usr/bin/python3
"""Beehive Model"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean
from slqalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from os import environ


# default time
default_time = datetime(1970, 1, 1)


class Beehive(BaseModel, Base):
    """Define beehive model"""

    # class level attribute to track the last used ID
    # _last_id = 0

    if models.storage_type == 'db':
        # use database
        __tablename__ = 'beehives'

        # override the UUID column with integer type
        apiary_id = Column(String(60), ForeignKey('apiaries.id'),
                           nullable=False)
        ready_for_harvest = Column(Boolean, default=False)
        next_harvest_date = Column(DateTime, default=default_time)
        harvest_count = Column(Integer, default=0)

        # Establish relationship with Inspection and Harvest
        inspections = relationship('Inspection', backref='beehive',
                                   cascade='all, delete-orphan')
        harvests = relationship('Harvest', backref='beehive',
                                cascade='all, delete-orphan')
    else:
        apiary_id = ""
        ready_for_harvest = False
        next_harvest_date = "TBD"
        harvest_count = 0

    def __init__(self, *args, **kwargs):
        """initialize beehive"""
        super().__init__(*args, **kwargs)
