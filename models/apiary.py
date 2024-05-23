#!/usr/bin/python3
""" Create an Apiary"""
from models.base_model import BaseModel
from models.beehive import Beehive
from models.user import User


class Apiary(BaseModel):
    """define an apiary"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs:
            # when loading from database
            if kwargs.get('name'):
                self.name = kwargs.get('name')
            if kwargs.get('location'):
                self.location = kwargs.get('location')
            if kwargs.get('user'):
                self.user = kwargs.get('user')
            if kwargs.get('county'):
                self.county = kwargs.get('county')
            if kwargs.get('town'):
                self.town = kwargs.get('town', "")
        else:
            self.name = ""
            self.location = ""
            self.user = ""


if __name__ == "__main__":
    beehive = Beehive()
    beehive1 = Beehive()
    beehive2 = Beehive()
    user1 = User("Julius", "Machira", 2000)
    apiary = Apiary("Kirwa C", (-73.935242, 40.730610), user1)
    apiary.add_beehive(beehive)
    apiary.add_beehive(beehive1)

    print(apiary.__dict__)
