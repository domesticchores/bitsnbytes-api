import datetime
import hashlib
import api.s3
import api.img
import json
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, TIMESTAMP, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Interaction(Base):
    __tablename__ = 'interaction_data'

    time = Column(TIMESTAMP, nullable=False, primary_key=True) # not actually primary key, workaround
    slot_id = Column(String, nullable=False)
    quantity_removed = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    
    def __init__(self, form_data):
        self.time = form_data['time']
        if self.time is None:
            raise ValueError("Warning: Missing Time")
        self.slot_id = form_data['slot_id']
        if self.slot_id is None:
            raise ValueError("Warning: Missing Slot")
        self.quantity_removed = form_data['quantity_removed']
        if self.quantity_removed is None:
            self.quantity_removed = 0
        self.item_id = form_data['item_id']
        if self.item_id is None:
            raise ValueError("Warning: Missing Item ID")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Vision(Base):
    __tablename__ = 'vision_data'

    vision_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    time = Column(TIMESTAMP, nullable=False, primary_key=True) # not actually primary key, workaround
    
    def __init__(self, form_data):
        self.vision_class = form_data['vision_class']
        if len(self.vision_class) == 0:
            raise ValueError("Warning: Missing vision_class")
        self.confidence = form_data['confidence']
        if self.confidence == None:
            raise ValueError("Warning: Missing Confidence")
        self.time = form_data['time']
        if self.time == None:
            raise ValueError("Warning: Missing Time")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def as_string_dict(self):
        base = self.as_dict()
        base["time"] = datetime.datetime.strftime(base["time"], "%Y-%m-%d %H:%M:%S.%f")
        return base

class Weight(Base):
    __tablename__ = 'weight_data'

    slot_id = Column(String, nullable=False)
    weight_grams  = Column(Double, nullable=False)
    time = Column(TIMESTAMP, nullable=False, primary_key=True) # not actually primary key, workaround
    
    def __init__(self, form_data):
        self.slot_id = form_data['slot_id']
        if self.slot_id == None:
            raise ValueError("Warning: Missing Slot ID")
        self.weight_grams = form_data['weight_grams']
        if self.weight_grams == None:
            raise ValueError("Warning: Weight (Grams)")
        self.time = form_data['time']
        if self.time == None:
            raise ValueError("Warning: Missing Time")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_string_dict(self):
        base = self.as_dict()
        base["time"] = datetime.datetime.strftime(base["time"], "%Y-%m-%d %H:%M:%S.%f")
        return base