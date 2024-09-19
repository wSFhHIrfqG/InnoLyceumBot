from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config_data import config

engine = create_engine(
	config.DATABASE_URL, connect_args={"check_same_thread": False}
)
engine.connect()

SessionLocal = sessionmaker(
	autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
