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
    
    def __init__(self):

        api.db.add(self)

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