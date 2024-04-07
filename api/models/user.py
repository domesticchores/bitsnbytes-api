from sqlalchemy import Column, Integer, String, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='Untitled')
    balance = Column(Integer, default=0)
    payment_type = Column(String, default="credit")
    token = Column(String, unique=True)
    email = Column(String, default="")
    phone = Column(String, default="")
    thumb_img = Column(String, default='http://placehold.jp/150x150.png')
    
    def __init__(self, form_data):
        self.name = form_data['name']
        if len(self.name) == 0:
            self.name = 'Untitled'
        self.thumb_img = form_data['thumb_img']
        if len(self.thumb_img) == 0:
            self.thumb_img = 'http://placehold.jp/150x150.png'
        self.balance = form_data['balance']
        if self.balance is None:
            self.balance = 0
        self.payment_type = form_data['payment_type']
        if self.payment_type not in ['credit', 'dining', 'imagine']:
            self.payment_type = "credit"
        self.token = form_data['token']
        if len(self.token) == 0:
            raise ValueError("Missing Token")
        self.email = form_data['email']
        if len(self.email) == 0:
            self.email = ""
        self.phone = form_data['phone']
        if len(self.phone) == 0:
            self.phone = ""

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
