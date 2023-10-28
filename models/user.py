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
    secret_question = Column(String(512), nullable=False)
    secret_answer = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    password = Column(String(512), nullable=False)
    salt_used = Column(String(60), nullable=False)
    inventories = relationship("Inventory", cascade='delete')

    def __init__(self, last_name, first_name, username, email, password,
                 secret_question, secret_answer):
        """ Initiates a User class."""
        self.salt_used = secrets.token_hex(16)
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.email = email
        self.update_password(password)
        self.set_secret_question(secret_question, secret_answer)
        self.created_at = datetime.utcnow()

    def update_password(self, password):
        """ Hashes the password and saves it. """
        salted_password = self.salt_used + password
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        self.password = hashed_password

    def verify_password(self, input_password):
        """ Checks if given password is correct. """
        salted_password = self.salt_used + input_password
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashed_password == self.password

    def set_secret_question(self, secret_question, secret_answer):
        """ Sets the secret_question and answer as an alternative login. """
        self.secret_question = secret_question
        salted_answer = self.salt_used + secret_answer
        hashed_answer = hashlib.sha256(salted_answer.encode()).hexdigest()
        self.secret_answer = hashed_answer

    def verify_secret_answer(self, secret_answer):
        """ Checks if given secret_answer is correct. """
        salted_answer = self.salt_used + secret_answer
        hashed_answer = hashlib.sha256(salted_answer.encode()).hexdigest()
        return hashed_answer == self.secret_answer

    def update_email(self, email):
        """ updates the user email address. """
        self.email = email
