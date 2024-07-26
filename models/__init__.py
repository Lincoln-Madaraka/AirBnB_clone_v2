#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')
if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
