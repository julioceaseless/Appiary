#!/usr/bin/python3
"""Harvest Model"""


import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from datetime import datetime


class Harvest(BaseModel, Base):
    """Define harvest class"""
    _last_id = 0

    if models.storage_type == 'db':
        # use database storage
        __tablename__ = 'harvests'

        # override the UUID column with integer ID
        id = Column(Integer, primary_key=True)

        hive_id = Column(Integer, ForeignKey('beehives.id'), nullable=False)
        quantity = Column(Float, default=0.00)
        notes = Column(String(1024), nullable=True)
    else:
        # use file storage
        hive_id = ''
        quantity = 0.00
        notes = ''

    def __init__(self, *args, **kwargs):
        """Initialize Harvest"""
        super().__init__(*args, **kwargs)
        if not kwargs.get('id'):
            Harvest._last_id += 1
            self.id = Harvest._last_id
        else:
            self.id = kwargs['id']

    def set_next_harvest(self):
        """modifies the Beehive object to schedule the next harvest date"""
        beehive = models.storage.get("Beehive", self.hive_id)
        if beehive:
            if beehive.ready_for_harvest:
                # reset ready flag
                beehive.ready_for_harvest = False

                # calculate the next harvest date
                current_month = datetime.now().month
                next_month = (current_month + 3) % 12
                next_year = datetime.now().year + (current_month + 3) / 12
                next_harvest_date = datetime(int(next_year),
                                             int(next_month),
                                             int(self.created_at.day)
                                             ).isoformat()

                # set next harvest date
                if hasattr(beehive, 'next_harvest_date'):
                    beehive.next_harvest_date = next_harvest_date
                else:
                    setattr(beehive, 'next_harvest_date', next_harvest_date)
                beehive.update()
            else:
                return f"{beehive.id} is not ready for harvest!"
        else:
            return "Error: Beehive not found."
