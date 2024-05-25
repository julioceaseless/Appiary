#!/usr/bin/python3
"""Beehive Model"""
import models
from models.base_model import BaseModel, Base
from os import environ
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime
from datetime import datetime

class Beehive(BaseModel, Base):
    """Define beehive model"""
    
    # class level attribute to track the last used ID
    _last_id = 0
    
    if models.storage_type == 'db':
        # use database
        __tablename__ = 'beehives'

        # override the UUID column with integer type
        id = Column(Integer, primary_key=True)
        apiary_id = Column(Integer, ForeignKey('apiaries.id'), nullable=False)
        ready_for_harvest = Column(Boolean, default=False)
        next_harvest_date = Column(DateTime, default=datetime.utcnow)

        # relationships
        # inspections = relationship('Inspection', back_populates='beehive')
        # harvests = relationship('Harvest', back_populates='beehive')
    else:
        apiary_id = ""
        ready_for_harvest = False
        next_harvest_date = "TBD"


    def __init__(self, *args, **kwargs):
        
        """initialize beehive"""
        super().__init__(*args, **kwargs)
        if not kwargs.get('id'):
            Beehive._last_id += 1
            self.id = str(Beehive._last_id)
        else:
            self.id = str(kwargs['id'])

        # self.inspections = []
        # self.harvests = []
    

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

