from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://', echo=True)

Base = declarative_base(metadata=MetaData(), bind=engine)

