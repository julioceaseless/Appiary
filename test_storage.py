#!/usr/bin/python3
""" test storage"""
from models import storage

storage.reload()
print(storage.all())
print(storage.objs())
