#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', ForeignKey('places.id'),
                             primary_key=True),
                      Column('amenity_id', ForeignKey('amenities.id'),
                             primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False, backref='place_amenities')
    reviews = relationship('Review', backref='place')
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            '''returns the list of Amenity instances'''
            from models.amenity import Amenity
            amenity = []
            for obj in models.storage.all(Amenity).values():
                if obj.id in Place.amenity_ids:
                    amenity.append(obj)
            return amenity

        @amenities.setter
        def amenities(self, obj):
            '''setter'''
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                Place.amenity_ids.append(obj.id)

        @property
        def reviews(self):
            '''return list of Reviews'''
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list
