from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = None

def make_declarative_base(uri, echo=False):
    global Base
    engine = create_engine(uri, echo=echo)
    Base = declarative_base(metadata=MetaData(), bind=engine)

