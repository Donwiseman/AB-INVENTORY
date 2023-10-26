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
    price = Column(Float)
    category = Column(String(128))

    def __init__(self, inventory_id, name, price, quantity=0, unit=None,
                 category=None):
        """ Initiates an item in an inventory. """
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.quantity = quantity
        self.unit = unit
        self.category = category
        self.inventory_id = inventory_id
