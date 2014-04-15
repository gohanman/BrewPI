from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from .. import config

engine = create_engine(config.DATABASE_URI)
engine.echo = True
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from BrewPi.data.models import *
    Base.metadata.create_all(bind=engine)

init_db()
