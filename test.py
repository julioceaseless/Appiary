#!/usr/bin/python3
"""Test file"""
from models import storage
from models.user import User
from models.apiary import Apiary
from models.beehive import Beehive
from models.inspection import Inspection
from models.harvest import Harvest
from time import sleep


# create user
user_attr = {"first_name": "Julius", "last_name": "Wamuyu",
             "yob": 1990, "email": "me@mymail.com"
            }
user = User(**user_attr)
storage.new(user)
storage.save()

# create apiary
apiary_attr = {"name": "Kigumo", "longitude": 2.2222,
               "latitude": 1.1111, "user_id": user.id,
               "description": "first set up"
               }
apiary = Apiary(**apiary_attr)
apiary.save()

for num in range(5):
    beehive_attr = {"apiary_id": apiary.id,
                    "hive_type": "langstroth",
                    "wood_type": "cypress"}
    beehive = Beehive(**beehive_attr)
    beehive.save()

# retrieve a beehive
beehive_keys = list(storage.all("Beehive").keys())
beehive_id = beehive_keys[1].split('.')[1]
beehive_id = "51dc9d2e-fc58-4a7e-8a09-1d7204b27359"
print(f"Beehive_ID: {beehive_id}")

print(storage.get("Beehive", beehive_id))
# inspection
insp_attr = {"hive_id": beehive_id, "observations": "This is a strong colony", "ready_for_harvest": True}
inspection = Inspection(**insp_attr)
sleep(5)
inspection.set_hive_status()
inspection.save()


# havest
new_beehive = storage.get("Beehive", beehive_id)
if new_beehive.ready_for_harvest():
    # record harvest details
    harvest_attr = {"hive_id": beehive_id, "quantity": 9.70, "notes": "bamper harvest"}
    harvest = Harvest(**harvest_attr)
    harvest.set_next_harvest()
    harvest.save()
