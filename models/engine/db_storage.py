#!/usr/bin/python3
'''Module contain DBStorage'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
classes = {
    'State': State, 'City': City, 'User': User,
    'Place': Place, 'Amenity': Amenity,
    'Review': Review
        }


class DBStorage:
    '''Class representation of database'''
    __engine = None
    __session = None

    def __init__(self):
        '''initialize the DB'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')
        ), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Return all the objects depending on the class'''
        cls_all = []
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            cls_all = self.__session.query(cls).all()
        else:
            for key, val in classes.items():
                cls_all.extend(self.__session.query(val).all())
        return {f'{val.__class__.__name__}.{val.id}': val for val in cls_all}

    def new(self, obj):
        '''Add obj to the session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes to the session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete obj from session'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''create all tables in the database'''
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        '''Close the current session'''
        self.__session.remove()
