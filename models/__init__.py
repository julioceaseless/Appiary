#!/usr/bin/python3
from os import environ

# get the storage type
storage_type = environ.get('APPIARY_TYPE_STORAGE')


if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = FileStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = DBStorage()


storage.reload()
