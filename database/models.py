from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, VARCHAR, Boolean, DateTime
from sqlalchemy.orm import relationship

from database.db import Base


class Role(Base):
	__tablename__ = 'Role'

	role_id = Column(Integer, primary_key=True, unique=True, nullable=False)
	title = Column(VARCHAR(50), nullable=False)
	description = Column(String, nullable=False)

	role = relationship('Employee', back_populates='about_role')


class Employee(Base):
	__tablename__ = 'Employee'

	employee_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	surname = Column(VARCHAR(50), nullable=False)
	name = Column(VARCHAR(50), nullable=False)
	middlename = Column(VARCHAR(50), nullable=False)
	role_id = Column(Integer, ForeignKey('Role.role_id'), nullable=False)

	about_role = relationship('Role', back_populates='role')


class RegistarationRequest(Base):
	__tablename__ = 'RegistrationRequest'

	request_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	from_name = Column(VARCHAR(50), nullable=False)
	from_username = Column(VARCHAR(50), nullable=False)


class Class(Base):
	__tablename__ = 'Class'

	class_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	class_name = Column(VARCHAR(10), unique=True)
	last_date = Column(DateTime)

	student_class = relationship('Student', back_populates='student')


class Student(Base):
	__tablename__ = 'Student'

	student_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	surname = Column(VARCHAR(50), nullable=False)
	name = Column(VARCHAR(50), nullable=False)
	middlename = Column(VARCHAR(50))
	class_id = Column(Integer, ForeignKey('Class.class_id'), nullable=False)

	student = relationship('Class', back_populates='student_class')
