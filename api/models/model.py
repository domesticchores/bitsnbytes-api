from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='Untitled User')
    thumb_img = Column(String, default='http://placehold.jp/150x150.png')
    balance = Column(Float, default=0.00)
    email = Column(String, default="")
    phone = Column(String, default="")
    nfc_data = relationship("NFC")
    
    def __init__(self, form_data):
        self.name = form_data['name']
        if len(self.name) == 0:
            self.name = 'Untitled User'
        self.balance = form_data['balance']
        if self.balance is None:
            self.balance = 0.00
        self.email = form_data['email']
        if len(self.email) == 0:
            self.email = ""
        self.phone = form_data['phone']
        if len(self.phone) == 0:
            self.phone = ""
        self.thumb_img = form_data['thumb_img']
        if len(self.thumb_img) == 0:
            self.thumb_img = 'http://placehold.jp/150x150.png'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class NFC(Base):
    __tablename__ = 'nfc_data'

    id = Column(String, primary_key=True)
    assigned_user = Column(Integer, ForeignKey("users.id"))
    type = Column(String, default='MIFARE')
    
    def __init__(self, form_data):
        self.id = form_data['id']
        if len(self.id) is None:
            raise ValueError("Warning: Missing NFC ID")
        self.assigned_user = form_data['assigned_user']
        if self.assigned_user is None:
            raise ValueError("Warning: Missing UID")
        self.type = form_data['type']
        if len(self.type) == 0:
            self.type = "MIFARE"

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}