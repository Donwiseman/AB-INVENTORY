""" Keeps track of all transactions carried in the inventory. """

from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float


class Transaction(Base):
    """ Defines details of a given transaction in the inventory. """
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow())
    transaction_type = Column(String(128), nullable=False),
    item = Column(String(128), nullable=False),
    quantity = Column(Integer, default=0)
    details = Column(String(128))

    def __init__(self, trans_type_code, item, quantity, details):
        """ Creates a transaction object. """
        if trans_type_code == 0:
            self.transaction_type = "Purchase or Addition"
        else:
            self.transaction_type = "Sale or Removal"
        self.item = item
        self.quantity = quantity
        self.details = details
        self.date = datetime.utcnow()
