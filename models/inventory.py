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
    timezone = Column(Integer, default=0)
    username = Column(String(128), ForeignKey('users.username'),
                      nullable=False)
    items = relationship("Item", cascade="delete")
    transactions = relationship("Transaction", cascade="delete")

    def __init__(self, name, username, timezone=0):
        """ Initializes an inventory for a user."""
        self.id = str(uuid.uuid4())
        self.name = name
        self.username = username
        self.timezone = timezone
