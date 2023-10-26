""" Handles ORM with SqlAlchemy for all classes. """
from models import Base, User, Inventory, Item, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database:
    """ Builds the database storage system to relate with the database. """
    __engine = None
    __sesssion = None
