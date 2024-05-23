#!/usr/bin/python3
""" Create an Apiary"""
from models.base_model import BaseModel
import models

class Beehive(BaseModel):
    """define an apiary"""
    count = 0

    def __init__(self, *args, **kwargs):
        """initialize beehive"""
        super().__init__(*args, **kwargs)
        self.id = str(Beehive.count)
        Beehive.count += 1
        self.apiary_id = kwargs.get('apiary_id')
        self.ready_for_harvest = False
        self.next_harvest_date = "TBD"
        self.inspections = []
        self.harvests = []
    

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

    def update_harvest_status(self, status):
        """update whether the beehive is ready for harvest"""
        if status == True: 
            self.ready_for_harvest = True
        else:
            self.ready_for_harvest = False


if __name__ == "__main__":
    apiary = Apiary()
    beehive = Beehive(apiary)
    beehive1 = Beehive()
    beehive2 = Beehive()
    print(beehive.to_dict())
    print(beehive1.to_dict())
    print(beehive2.to_dict())
    print(beehive2.__class__)
    print(beehive2.__class__.__name__)
