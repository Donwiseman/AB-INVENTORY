""" This defines the Inventory class which handles Inventory manipulation. """

from models import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


class Inventory(Base):
    """ This defines the Inventory class and implements methods for
        handling varius Inventory actions.
    """
    __tablename__ = 'inventories'
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)
    timezone = Column(String(60), primary_key=True)
    username = Column(String(128), ForeignKey('users.username'),
                      nullable=False)
    items = relationship("Item", cascade="delete")
    transactions = relationship("Transaction", cascade="delete")

    def __init__(self, name, username, timezone):
        """ Initializes an inventory for a user."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.timezone = timezone

    def search_item(self, item_name):
        """ search items in inventory based on item name. """
        result = []
        for item in self.items:
            if item_name == item.name[:len(item_name)]:
                result.append(item)
        return result

    def add_item(self, item, quantity, purchase_cost=-1, details=None):
        """ Adds more quantity of an item. """
        from models import storage, Transaction

        new_quantity = item.add(quantity)
        if details is None:
            details = f"{quantity} {item.name} was added to {self.name}"
        trans = Transaction(self.id, self.timezone, 0, item, quantity,
                            new_quantity, purchase_cost, details)
        storage.add(trans)
        storage.save()
        return trans

    def remove_item(self, item, quantity, details=None):
        """ Adds more quantity of an item. """
        from models import storage, Transaction

        new_quantity = item.remove(quantity)
        if new_quantity == -1:
            return None
        if details is None:
            details = f"{quantity} {item.name} was removed from {self.name}"
        trans = Transaction(self.id, self.timezone, 1, item, quantity,
                            new_quantity, -1,  details)
        storage.add(trans)
        storage.save()
        return trans

    def delete_item(self, item, loss=-1):
        """ deletes an item from the inventory. """
        from models import storage, Transaction

        details = f"{item.quantity} {item.name} was removed and {item.name} \
deleted from {self.name} list"
        trans = Transaction(self.id, self.timezone, 1, item,
                            item.quantity, 0, loss, details)
        storage.delete(item)
        storage.add(trans)
        storage.save()
        return trans

    def create_item(self, name, cost_price, sale_price, quantity=0,
                    trans_val=-1, unit=None, category=None, alert_level=0):
        """ Adds an item to the inventory. """
        from models import storage, Item, Transaction

        details = f"Created {name} item and add {quantity} to {self.name}"
        item = Item(self.id, name, cost_price, sale_price, quantity,
                    unit, category, alert_level)
        storage.add(item)
        trans = Transaction(self.id, self.timezone, 0, item,
                            item.quantity, item.quantity, trans_val, details)
        storage.add(trans)
        storage.save()
        return item

    def get_transactions(self, start_date, end_date, item_name=None):
        """ Returns a list of transactions for the date duration. """
        tr_list = [trans for trans in self.transactions if start_date <=
                   trans.date <= end_date]
        if item_name:
            fi_list = [trans for trans in tr_list if item_name == trans.item]
            return fi_list
        return tr_list

    def get_a_transaction(self, tran_id):
        """ Returns a specific transaction. """
        for transaction in self.transactions:
            if transaction.transaction_id == tran_id:
                return transaction
        return None

    def set_alert_all(self, quantity):
        """ sets the alert level for low amount for all items in inventory"""
        from models import storage

        for item in self.items:
            item.alert_level = quantity
            storage.add(item)
        storage.save()
        return True

    def trigger_alerts(self):
        """ Trigger alerts for all item low in the inventory. """
        alerts = []
        for item in self.items:
            if item.trigger_alert():
                alerts.append(item)
        return alerts
