from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, VARCHAR, Date, Boolean
from sqlalchemy.orm import relationship

from database.db import Base


class Role(Base):
	__tablename__ = 'Role'

	role_id = Column(Integer, primary_key=True, unique=True, nullable=False)
	title = Column(VARCHAR(50), nullable=False)
	description = Column(String, nullable=False)

	role = relationship('Employee', back_populates='about_role')

	def __str__(self):
		return f'{self.role_id} {self.title} {self.description}'


class Employee(Base):
	__tablename__ = 'Employee'

	employee_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	surname = Column(VARCHAR(50), nullable=False)
	name = Column(VARCHAR(50), nullable=False)
	middlename = Column(VARCHAR(50), nullable=False)
	role_id = Column(Integer, ForeignKey('Role.role_id'), nullable=False)

	about_role = relationship('Role', back_populates='role')

	def __str__(self):
		return f'{self.employee_id} {self.telegram_id} {self.surname} {self.name} {self.middlename} {self.role_id}'


class RegistarationRequest(Base):
	__tablename__ = 'RegistrationRequest'

	request_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	from_name = Column(VARCHAR(50), nullable=False)
	from_username = Column(VARCHAR(50), nullable=False)

	def __str__(self):
		return f'{self.request_id} {self.telegram_id} {self.from_name} {self.from_username}'


class Class(Base):
	__tablename__ = 'Class'

	class_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	class_name = Column(VARCHAR(10), unique=True)
	last_date = Column(Date)

	student_class = relationship('Student', back_populates='student')

	def __str__(self):
		return f'{self.class_id} {self.class_name} {self.last_date}'


class Student(Base):
	__tablename__ = 'Student'

	student_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	surname = Column(VARCHAR(50), nullable=False)
	name = Column(VARCHAR(50), nullable=False)
	middlename = Column(VARCHAR(50))
	class_id = Column(Integer, ForeignKey('Class.class_id'), nullable=False)

	student = relationship('Class', back_populates='student_class')
	absent_student = relationship('Absent', back_populates='about_student')

	def __str__(self):
		return f'{self.student_id} {self.surname} {self.name} {self.middlename} {self.class_id}'


class BlockedUser(Base):
	__tablename__ = 'BlockedUser'

	blocked_user_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False, unique=True)

	def __str__(self):
		return f'{self.blocked_user_id} {self.telegram_id}'


class AbsenceReason(Base):
	__tablename__ = 'AbsenceReason'

	reason_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	title = Column(VARCHAR(100), nullable=False)
	description = Column(String, nullable=False)
	in_lyceum = Column(Boolean, nullable=False)

	reason = relationship('Absent', back_populates='absent')

	def __str__(self):
		return f'{self.reason_id} {self.title} {self.description} {self.in_lyceum}'


class Absent(Base):
	__tablename__ = 'Absent'

	absent_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	reason_id = Column(Integer, ForeignKey('AbsenceReason.reason_id'), nullable=False)
	student_id = Column(Integer, ForeignKey('Student.student_id'), nullable=False)
	date = Column(Date)

	absent = relationship('AbsenceReason', back_populates='reason')
	about_student = relationship('Student', back_populates='absent_student')

	def __str__(self):
		return f'{self.absent_id} {self.reason_id} {self.student_id} {self.date}'
