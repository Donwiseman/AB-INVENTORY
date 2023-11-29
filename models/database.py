""" Handles ORM with SqlAlchemy for all classes. """
from models import Base, User, Inventory, Item, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database:
    """ Builds the database storage system to relate with the database. """
    __engine = None
    __session = None

    def __init__(self, sql_user, sql_password, db_name):
        """ Initializes ORM. """
        self.__engine = create_engine(f"mysql+mysqldb://{sql_user}:\
{sql_password}@localhost/{db_name}",  pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

    def add(self, obj):
        ''' Adds the object to the current database session '''
        self.__session.add(obj)

    def save(self):
        ''' Commit all changes to the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        ''' Deletes from the current database session obj if not None.'''
        if obj is not None:
            self.__session.delete(obj)

    def start_session(self):
        """ Starts a new scoped session. """
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def end_session(self):
        """ Ends the scoped session and allows for a new one to start. """
        self.__session.remove()

    def get_users(self, username=None):
        """ Get all registred users or a specified user. """
        if username:
            return self.__session.query(User).filter(User.username == username
                                                     ).all()
        else:
            return self.__session.query(User).all()

    def get_user_inventories(self, username):
        """ Returns a list of specifies user inventory."""
        return self.__session.query(Inventory).filter(Inventory.username ==
                                                      username).all()

    def get_inventory(self, inventory_id):
        """ Return a list containing the specified Inventory. """
        return self.__session.query(Inventory).filter(Inventory.id ==
                                                      inventory_id).all()

    def get_item(self, item_id):
        """ Return a list containing the specified Inventory. """
        return self.__session.query(Item).filter(Item.id == item_id).all()

    def user_via_email(self, email):
        """ Get user via their email. """
        return self.__session.query(User).filter(User.email == email).all()
