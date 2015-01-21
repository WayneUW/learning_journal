import datetime

from cryptacular.bcrypt import BCRYPTPasswordManager as Manager    # import but bind to a different symbol

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    )

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session( sessionmaker( extension=ZopeTransactionExtension( ) ) )
Base = declarative_base( )

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Entry( Base ):
    __tablename__ = 'entries'
    id = Column( Integer, primary_key=True )
    title = Column( Unicode(255), unique=True, nullable=False)
    body = Column( UnicodeText, default=u' ' )   # check the u with single quotes
    created = Column( DateTime, default=datetime.datetime.utcnow )
    edited = Column( DateTime, default=datetime.datetime.utcnow )    # Is there a way to do this without time?


    # def __init__( self, title, body, edited, created ):    # self is an instance of the class for which you will need to create a method for it. Instead you use the @classmethod to pass the class object.
    #     self.title = title
    #     self.body = body
    #     self.edited = edited
    #     self.created = created

    @classmethod
    def all(cls, session=None):    # cls is more generic instead of using the class name as the argument
        if session is None:    # this is to help when you are using the command line
            session = DBSession
        return session.query(cls).order_by(sa.desc(cls.created)).all( )    # is the return for DBSession or just session?

    @classmethod
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).get(id)    # is the return for DBSession or just session?


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    
    @classmethod
    def by_name(cls, name, session=None):
        if session is None:
            session = DBSession
        return DBSession.query(User).filter(cls.name == name).first()    # looking for a name, take the first one and hand it back to ourselves
    
    def verify_password(self, password):
        manager = Manager()
        return manager.check(self.password, password)

    


"""
query 1
def return_all( ):
    allrows = session.query( Entry ).all( ).order_by( Entry.created) # with all the query hits the db and the results are returned
    print allrows

query 2
def by_id( id_name ):
    one_entry = session.query( Entry ).get( Id_name )
    print one_entry

"""

"""
Wayne TTD
-Check on the first argument for Index
-Define a method "all( )" that returns all entries in the db ordered by most recent
-Define a method "by_id" that returns a single entry by id
"""
