from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()
engine = create_engine('sqlite:///blog.db')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
