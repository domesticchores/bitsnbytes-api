import hashlib
import api.s3
import api.img
import json
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'  # Name of the database table

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='Untitled')
    thumb_img = Column(String, default='http://placehold.jp/150x150.png')
    weight_avg = Column(Float, default=0.0)
    weight_std = Column(Float, default=0.0)
    vision_class = Column(String)
    upc = Column(String, default='0000000000')
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    
    def __init__(self, form_data):
        self.name = form_data['name']
        if len(self.name) == 0:
            raise ValueError("Missing Name")
        self.thumb_img = form_data['thumb_img']
        if len(self.thumb_img) == 0:
            self.thumb_img = 'http://placehold.jp/150x150.png'
        self.weight_avg = form_data['weight_avg']
        if self.weight_avg is None:
            self.weight_avg = 0.0
        self.weight_std = form_data['weight_std']
        if self.weight_std is None:
            self.weight_std = 0.0
        self.vision_class = form_data['vision_class']
        if self.vision_class is None:
            raise ValueError("Missing vision_class")
        self.upc = form_data['upc']
        if len(self.upc) == 0:
            self.upc = '0000000000'
        self.quantity = form_data['quantity']
        if self.quantity is None:
            self.quantity = 0
        self.price = form_data['price']
        if self.price is None:
            self.price = 0.0

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def add_image(file):
        """
        Processes image, adds to s3 and db
        """
        fullsizehash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)

        s3.upload_file(fullsizehash, file)

        with Image.open(file) as im:
            im = img.crop_center