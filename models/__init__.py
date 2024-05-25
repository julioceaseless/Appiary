#!/usr/bin/python3
"""
initialize the models package
"""
from os import environ


# get the storage type from environment
storage_type = environ.get('APPIARY_TYPE_STORAGE')

# select engine based on the storage type
if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# reload objects from storage
storage.reload()
