#!/usr/bin/python3
"""Beehive Model"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy import ForeignKey, DateTime
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
        _ready_for_harvest = Column(Boolean, default=False)
        _next_harvest_date = Column(DateTime, default=default_time)
        _harvest_count = Column(Integer, default=0)
        hive_type = Column(String(60), nullable=False)
        wood_type = Column(String(60), nullable=False)

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

    @property
    def ready_for_harvest(self):
        '''Getter for ready_for_harvest'''
        return self._ready_for_harvest

    @property
    def next_harvest_date(self):
        '''Getter for next_harvest_date'''
        return self._next_harvest_date

    @property
    def harvest_count(self):
        '''Getter for harvest_count'''
        return self._harvest_count

    def update_status(self, ready_for_harvest):
        '''Method to update if hive is ready for harvest'''
        self._ready_for_harvest = ready_for_harvest

    def update_harvest_info(self, next_harvest_date,
                            harvest_count):
        '''Method to update harvest info internally'''
        self._next_harvest_date = next_harvest_date
        self._harvest_count = harvest_count
