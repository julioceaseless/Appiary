#!/usr/bin/python3
"""Test file"""
from models import storage
from models.user import User
from models.apiary import Apiary
from models.beehive import Beehive
from models.inspection import Inspection
from models.harvest import Harvest

# create user
user_attr = {"first_name": "Julius", "last_name": "Wamuyu", "yob": "1990"}
user = User(**user_attr)
storage.new(user)

# create apiary
apiary_attr = {"name": "Kigumo", "location": "Nyahururu", "user": "Julius"}
apiary = Apiary(**apiary_attr)
storage.new(apiary)

# create beehive
hive_attr = {"apiary_id": "becf6c14-ebdc-41b0-a371-9efc3ccac78b"}
beehive = Beehive(**hive_attr)
storage.new(beehive)

# inspect hive
insp_attr = {"hive_id": "3", "notes": "the hive is full. Needs to be harvested", "hive_status": True}
try:
    inspection = Inspection(**insp_attr)
    if not inspection.hive_status:
        raise ValueError("Hive not ready!")
    inspection.set_harvest_ready()
except Exception as e:
    print(e)
storage.new(inspection)

# harvest honey
harv_attr = {"hive_id": "3", 'notes': "All frames are filled and capped", "quantity": 20, "nothing": "gibberish"}
harvest = Harvest(**harv_attr)
storage.new(harvest)

# set the next harvest date
harvest.next_harvest()

'''
# add new objects to objects dictionary
storage.new(apiary)
storage.new(user)
storage.new(beehive)

storage.new(inspection)
storage.new(harvest)
'''
# save the changes
storage.save()

print("----------View Profile-------------")
print(user.view_profile())
print("----------all----------------------")
print(storage.all(Beehive))
print("----------get----------------------")
print(storage.get("Beehive", "1"))
print(storage.get("Beehive", "3"))

