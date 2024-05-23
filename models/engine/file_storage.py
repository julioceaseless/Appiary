#!/usr/bin/python3
""" file storage"""
import json
from models.base_model import BaseModel
from models.beehive import Beehive
from models.apiary import Apiary
from models.inspection import Inspection
from models.user import User
from models.harvest import Harvest



classes = {
        'BaseModel': BaseModel, 'Apiary': Apiary, 'User': User, 
        'Inspection': Inspection, 'Beehive': Beehive, 'Harvest':Harvest
        }


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        if cls is not None:
            if not isinstance(cls, str):
                # retrieve class name
                cls = cls.__name__
            filtered_objs = {}
            for key, value in FileStorage.__objects.items():
                if cls == value.__class__.__name__:
                    filtered_objs[key] = value
            return filtered_objs
        return FileStorage.__objects


    def new(self, obj):
        """create new object"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            FileStorage.__objects[key] = obj


    def save(self):
        """Serialize object to JSON data"""
        temp = {}
        for key, value in FileStorage.__objects.items():
            temp[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(temp, f)
   

    def reload(self):
        """deserialize JSON data to objects"""
        try:
            with open(FileStorage.__file_path, 'r', encoding="UTF-8") as f:
                # retrieve json objects from file
                j_objs = json.load(f)
                for key, value in j_objs.items():
                    # get class name for each object
                    obj_cls_name = value.get("__class__")
                    if obj_cls_name:
                        # retrieve the class
                        obj_class = classes.get(obj_cls_name)
                        if obj_class:
                            # create key-value pairs of attributes for each object
                            obj_attr = {k: v for k, v in value.items()}
                            # recreate an instance
                            obj_instance = obj_class(**obj_attr)
                            # store the instance
                            FileStorage.__objects[key] = obj_instance
                        else:
                            print(f"class {obj_cls_name} not found")
                    else:
                        print(f"__class__ attribute missing")
        except FileNotFoundError:
            pass


    def delete(self, id):
        """delete object by UUID passed as argument"""
        if id is not None:
            # create key
            delete_keys = []
            for key in FileStorage.__objects:
                if key.split('.')[1] == id:
                    delete_keys.append(key)
            for key in delete_keys:
                FileStorage.__objects.pop(key)


    def get(self, cls_name, id):
        """retrieve an object by ID"""
        if cls_name:
            cls = classes.get(cls_name)
            if cls:
                all_objects = self.all(cls)
                for key in all_objects:
                    if (key.split('.')[1] == id):
                        return all_objects.get(key)
        return None


if __name__ == "__main__":
    filestorage = FileStorage()
