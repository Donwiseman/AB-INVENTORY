from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from models.user import User
from models.inventory import Inventory
from models.item import Item
from models.transaction import Transaction
from models.database import Database


storage = Database('ab_inventory', 'ab_123', 'ab_inventory_db')
storage.start_session()
