from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship
from api.models.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True))
    sent_sms = Column(Boolean)
    sent_email = Column(Boolean)
    transaction_start = Column(DateTime(timezone=True))
    transaction_end = Column(DateTime(timezone=True))
    receipt_sms_time = Column(BigInteger)
    receipt_email_time = Column(BigInteger)
    recorded_image_data = Column(Boolean)
    canceled = Column(Boolean)
    
    def __init__(self, form_data):
        self.user_id = form_data['user_id']
        if self.user_id is None:
            raise ValueError("Missing user_id")

        self.created_at = form_data['created_at']
        if self.created_at is None:
            raise ValueError("Missing created_at")

        self.transaction_start = form_data['transaction_start']
        if self.transaction_start is None:
            return ValueError("Missing transaction_start")
        self.transaction_end = form_data['transaction_end']
        if self.transaction_end is None:
            return ValueError("Missing transaction_end")

        self.sent_sms = form_data['sent_sms']
        if self.sent_sms is None:
            raise ValueError("missing sent_sms")

        self.sent_email = form_data['sent_email']
        if self.sent_email is None:
            raise ValueError("Missing sent_email")

        self.receipt_sms_time = form_data['receipt_sms_time']
        if self.receipt_sms_time is None:
            raise ValueError("missing receipt_sms_time")

        self.receipt_email_time = form_data['receipt_email_time']
        if self.receipt_email_time is None:
            raise ValueError("Missing receipt_email_time")

        self.recorded_image_data = form_data['recorded_image_data']
        if self.recorded_image_data is None:
            raise ValueError("missing recorded_image_data")

        self.canceled = form_data['canceled']
        if self.canceled is None:
            raise ValueError("Missing canceled")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TransactionItem(Base):
    __tablename__ = 'transaction_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True))

    def __init__(self, form_data):
        self.item_id = form_data['item_id']
        if self.item_id is None:
            raise ValueError("Missing item_id")

        self.transaction_id = form_data['transaction_id']
        if self.transaction_id is None:
            raise ValueError("Missing transaction_id")

        self.quantity = form_data['quantity']
        if self.quantity is None:
            raise ValueError("Missing quantity")

        self.created_at = form_data['created_at']
        if self.created_at is None:
            raise ValueError("Missing created_at")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
