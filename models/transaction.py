""" Keeps track of all transactions carried in the inventory. """

from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
import pytz


class Transaction(Base):
    """ Defines details of a given transaction in the inventory. """
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(String(60), ForeignKey('inventories.id'),
                          nullable=False)
    date = Column(DateTime, default=datetime.utcnow())
    transaction_type = Column(String(128), nullable=False)
    item = Column(String(128), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_quantity_after_transaction = Column(Integer, nullable=False)
    transaction_value = Column(Float, nullable=False)
    details = Column(String(128))

    def __init__(self, inventory_id, timezone, trans_type_code, item, quantity,
                 items_left, trans_value=-1, details=None):
        """ Creates a transaction object. """
        if trans_type_code == 0:
            self.transaction_type = "Purchase or Addition"
            if trans_value == -1:
                self.transaction_value = quantity * item.cost_price
            else:
                self.transaction_value = trans_value
        else:
            self.transaction_type = "Sale or Removal"
            if trans_value == -1:
                self.transaction_value = quantity * item.sale_price
            else:
                self.transaction_value = trans_value
        desired_tz = pytz.timezone(timezone)
        date_now = datetime.utcnow()
        self.date = date_now.replace(tzinfo=pytz.utc).astimezone(desired_tz)
        self.inventory_id = inventory_id
        self.item = item.name
        self.quantity = quantity
        self.item_quantity_after_transaction = items_left
        self.details = details

    def print_transaction(self):
        """ Returns the transaction details as dictionary. """
        return {
                'Date': self.date,
                'Transaction ID': self.transaction_id,
                'Transaction Type': self.transaction_type,
                'Item': self.item,
                'Quantity': self.quantity,
                'Amount': self.transaction_value
        }
