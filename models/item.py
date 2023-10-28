""" Represent an Item in an inventory. """

from models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
import uuid


class Item(Base):
    """ Defines an item in the Inventory. """
    __tablename__ = 'items'
    id = Column(String(60), primary_key=True)
    inventory_id = Column(String(60), ForeignKey("inventories.id"),
                          nullable=False)
    name = Column(String(128), nullable=False)
    quantity = Column(Integer, default=0)
    unit = Column(String(128))
    cost_price = Column(Float)
    sale_price = Column(Float)
    category = Column(String(128))
    alert_level = Column(Integer, default=0)

    def __init__(self, inventory_id, name, cost_price, sale_price, quantity,
                 unit=None, category=None, alert_level=0):
        """ Initiates an item in an inventory. """
        self.id = str(uuid.uuid4())
        self.name = name
        self.cost_price = cost_price
        self.sale_price = sale_price
        self.quantity = quantity
        self.unit = unit
        self.category = category
        self.inventory_id = inventory_id
        self.alert_level = alert_level

    def add(self, quantity):
        """ Adds given quantity of item to the inventory. """
        self.quantity += quantity
        return self.quantity

    def remove(self, quantity):
        """ Removes given quantity from the item. """
        if self.quantity >= quantity:
            self.quantity -= qunatity
            return self.quantity
        return -1

    def set_alert(self, alert_level):
        """ Sets the alert level for low quantity for this given item."""
        self.alert_level = alert_level
        return True

    def trigger_alert(self):
        """ Checks if item level is low. """
        if self.quantity <= self.alert_level:
            return True
        return False
