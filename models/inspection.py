#!/usr/bin/python3
"""Inspection class"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Inspection(BaseModel, Base):
    """Define inspection class"""
    if models.storage_type == 'db':
        # use database
        __tablename__ = 'inspections'

        hive_id = Column(Integer, ForeignKey('beehives.id'), nullable=False)
        observations = Column(String(1024), nullable=True)
        ready_for_harvest = Column(Boolean, default=False)
    else:
        # use file storage
        hive_id = ''
        observations = ''
        ready_for_harvest = ''

    def __init__(self, *args, **kwargs):
        """Initialize inspection"""
        super().__init__(*args, **kwargs)

    def validate_hive(self):
        """ check if hive is valid"""
        if self.hive_id:
            beehive = models.storage.get("Beehive", self.hive_id)
            if beehive:
                return True
        return False

    def update_notes(self, update_text):
        """update the observations"""
        if update_text:
            self.notes = update_text
            self.updated_at = datetime.now()

    def set_harvest_ready(self):
        """set harvest status"""
        beehive = models.storage.get("Beehive", self.hive_id)
        if beehive:
            if hasattr(beehive, 'ready_for_harvest'):
                beehive.ready_for_harvest = self.ready_for_harvest
            else:
                setattr(beehive, 'ready_for_harvest', self.ready_for_harvest)
            beehive.update()
        else:
            return f"Beehive does not exist"
