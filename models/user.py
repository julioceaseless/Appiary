#!/usr/bin/python3
"""User Profile"""
from models.base_model import BaseModel
from datetime import datetime

class User(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.yob = int(kwargs.get("yob"))
    about = ""


    @property
    def age(self):
        """create age property from yob and current year"""
        current_year = datetime.now().year
        if self.yob > 0 and (current_year - self.yob) > 1:
            return current_year - self.yob
        else:
            return 0

    def view_profile(self):
        """show user information"""
        user_info = {}
        for key, value in self.__dict__.items():
            if key not in ['id', 'updated_at', '__class__']:
                if key == "created_at":
                    user_info["Joined"] = f'{value.strftime("%B")}, {value.year}'
                    continue
                user_info[key] = value
        user_info['age'] = self.age
        return user_info


if __name__ == "__main__":
    user = User("Julius", "Machira", 2000)
    user1 = User()
    user1.yob = 1990
    user1.first_name = "Christie"
    print(user.__dict__)
    print("----------View Profile-------------")
    print(user.view_profile())


