#!/usr/bin/python3
"""Test file"""
from models import storage
from models.user import User
from models.apiary import Apiary
from models.beehive import Beehive



# create user
user_attr = {"first_name": "Julius", "last_name": "Wamuyu",
             "yob": 1990, "email": "me@mymail.com"
            }
user = User(**user_attr)
storage.new(user)
storage.save()

# create apiary
apiary_attr = {"name": "Kigumo", "longitude": 2.2222,
               "latitude": 1.1111, "user_id":user.id,
               "description": "first set up"
               }
apiary = Apiary(**apiary_attr)
storage.new(apiary)
storage.save()

for num in range(5):
    beehive_attr = {"apiary_id": apiary.id}
    beehive = Beehive(**beehive_attr)
    storage.new(beehive)
storage.save()

