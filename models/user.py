""" This is defines the User class which handles user authenticaton. """

from models import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float,\
        Table
from sqlalchemy.orm import relationship
import hashlib
import secrets


class User(Base):
    """ This defines a User and various properties about the user. """
    __tablename__ = 'users'
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    username = Column(String(60), primary_key=True)
    email = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    password = Column(String(512), nullable=False)
    salt_used = Column(String(60), nullable=False)
    inventories = relationship("Inventory", cascade='delete')

    def __init__(self, last_name, first_name, username, email, password):
        """ Initiates a User class."""
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.email = email
        self.hash_password(password)
        self.created_at = datetime.utcnow()

    def hash_password(self, password):
        """ Hashes the password and returns hash and salt used. """
        salt = secrets.token_hex(16)
        salted_password = salt + password
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        self.password = hashed_password
        self.salt_used = salt


    def verify_password(self, input_password):
        """ Checks if given password is correct. """
        salted_password = self.salt_used + input_password
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password == self.password
