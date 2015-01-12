import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session( sessionmaker( extension=ZopeTransactionExtension( ) ) )
Base = declarative_base( )


class Entry( Base ):
    __tablename__ = 'entries'
    id = Column( Integer, primary_key=True )
    title = Column( Text, nullable=False)
    body = Column( Integer, Unicode )
    edited = Column( DateTime, default=datetime.datetime.utcnow )
    created = Column( DateTime, default=datetime.datetime.utcnow )

    def __init__( self, title, body, edited, created ):
        self.title = title
        self.body = body
        self.edited = edited
        self.created = created

    def all( ):
        pass

    def by_id( ):
        pass

Index('my_index', Entry.title, unique=True, mysql_length=255)

Base.metadat.create_all( engine )


"""
Wayne TTD
-Check on the first argument for Index
-Define a method "def all( )" that returns all entries in the db ordered by most recent
-Define a method "def by_id" that returns a single entry by id
"""
