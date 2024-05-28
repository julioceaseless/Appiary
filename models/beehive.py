#!/usr/bin/python3
"""Beehive Model"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime
from datetime import datetime
from os import environ


# default time
default_time = datetime(1970, 1, 1)

class Beehive(BaseModel, Base):
    """Define beehive model"""
    
    # class level attribute to track the last used ID
    _last_id = 0
    
    if models.storage_type == 'db':
        # use database
        __tablename__ = 'beehives'

        # override the UUID column with integer type
        id = Column(Integer, primary_key=True, autoincrement=True)
        apiary_id = Column(String(60), ForeignKey('apiaries.id'), nullable=False)
        ready_for_harvest = Column(Boolean, default=False)
        next_harvest_date = Column(DateTime, default=default_time)
        harvest_count = Column(Integer, default=0)

        # relationships
        # inspections = relationship('Inspection', back_populates='beehive')
        # harvests = relationship('Harvest', back_populates='beehive')
    else:
        apiary_id = ""
        ready_for_harvest = False
        next_harvest_date = "TBD"
        harvest_count = 0


    def __init__(self, *args, **kwargs):
        
        """initialize beehive"""
        super().__init__(*args, **kwargs)
        if models.storage_type != 'db':
            if 'id' not in kwargs:
                Beehive._last_id += 1
                self.id = Beehive._last_id
            else:
                self.id = int(kwargs['id'])
        else:
            if 'id' in kwargs:
                self.id = int(kwargs['id'])

            # Set instance attributes using kwargs or class-level defaults
        self.apiary_id = kwargs.get('apiary_id', self.__class__.apiary_id)
        self.ready_for_harvest = kwargs.get('ready_for_harvest', self.__class__.ready_for_harvest)
        self.next_harvest_date = kwargs.get('next_harvest_date', self.__class__.next_harvest_date)
        self.harvest_count = kwargs.get('harvest_count', self.__class__.harvest_count)

    '''
    def add_inspection(self, inspection):
        """record inspections"""
        if not isinstance(inspection, Inspection):
            raise TypeError("Expected an object")
        else:
            self.inspection.append(inspection)


    def add_harvest(self, harvest):
        """record harvests"""
        if not isinstance(harvest, Harvest):
            raise TypeError("Expected an object")
        else:
            self.harvests.append(harvest)
    '''

    
    def update_harvest_status(self, status):
        """update whether the beehive is ready for harvest"""
        if status == True: 
            self.ready_for_harvest = True
        else:
            self.ready_for_harvest = False

