from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from models.user import User
from models.inventory import Inventory
from models.item import Item
from models.transaction import Transaction
