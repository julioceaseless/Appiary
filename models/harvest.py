#!/usr/bin/python3
"""Harvests"""

from datetime import datetime
from models.base_model import BaseModel
from models.beehive import Beehive
import models

class Harvest(BaseModel):
    """ record honey harvests"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valid_keys = ['hive_id', 'quantity', 'notes']
        valid_kwargs = {key: value for key, value in kwargs.items() if key in valid_keys}
        self.__dict__.update(valid_kwargs)

    
    def next_harvest(self):
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
                next_harvest_date = datetime(int(next_year), int(next_month), int(self.created_at.day)).isoformat()
                
                # set next harvest date
                if hasattr(beehive, 'next_harvest_date'):
                    beehive.next_harvest_date = next_harvest_date
                else:
                    setattr(beehive, 'next_harvest_date', next_harvest_date)
                return next_harvest_date
            else:
                return f"{beehive.id} is not ready for harvest!"
        else:
            return "Error: Beehive not found."


if __name__ == "__main__":
    beehive = Beehive("1234")
    harvest = Harvest(beehive)
    print(harvest.__dict__)
    print("---------------beehive--------------------")
    print(beehive.__dict__)
    
