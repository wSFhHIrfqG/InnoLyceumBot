from sqlalchemy import Column
from sqlalchemy import Integer, String, VARCHAR, Boolean

from database.db import Base


class Role(Base):
	__tablename__ = 'role'

	role_id = Column(Integer, primary_key=True, unique=True, nullable=False)
	title = Column(VARCHAR(50), nullable=False)
	description = Column(String, nullable=False)
