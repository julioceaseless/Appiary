#!/usr/bin/python3
"""Record harvests"""
from models.base_model import BaseModel
from datetime import datetime
import models


class Inspection(BaseModel):
    """ harvests management"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hive_id = kwargs.get('hive_id')
        self.notes = kwargs.get('notes')
        self.hive_status = kwargs.get('hive_status')
        self.valid_hive = self.validate_hive()


    def validate_hive(self):
        if self.hive_id:
            beehive = models.storage.get("Beehive", self.hive_id)
            if beehive:
                return True
        return False


    def update_notes(self, update_text):
        """update the notes"""
        if update_text:
            self.notes = update_text
            self.updated_at = datetime.now()

    def set_harvest_ready(self):
        """set harvest ready"""
        beehive = models.storage.get("Beehive", self.hive_id)
        if beehive:
            if hasattr(beehive, 'ready_for_harvest'):
                beehive.ready_for_harvest = self.hive_status
            else:
                setattr(beehive, 'ready_for_harvest', self.hive_status)
        else:
            return f"Beehive does not exist"
        

if __name__ == "__main__":
    inspection = Inspection("HIVE-002", "Good condition")
    print(inspection.to_dict())
    inspection.update_notes("Ants trying to enter the colony")
    print(inspection.to_dict())
