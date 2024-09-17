from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config_data import config

DATABASE_URL = config.DATABASE_URL

engine = create_engine(
	DATABASE_URL, connect_args={"check_same_thread": False}
)
engine.connect()

SessionLocal = sessionmaker(
	autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
