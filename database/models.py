from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import Integer, String, VARCHAR, Date, Boolean
from sqlalchemy.orm import relationship

from database.db import Base


class Role(Base):
	"""
	Роли сотрудников.

	Присваивается каждому сотруднику при парсинге.

	Колонки:
		employee_id: Идентификатор роли
		title: Название роли
		description: Описание роли
	"""
	__tablename__ = 'Role'

	role_id = Column(Integer, primary_key=True, unique=True, nullable=False)
	title = Column(VARCHAR(50), nullable=False)
	description = Column(String, nullable=False)

	employee = relationship('EmployeeRole', back_populates='about_role')

	def __str__(self):
		return f'{self.role_id} {self.title} {self.description}'


class Employee(Base):
	"""
	Сотрудники.

	Колонки:
		employee_id: Идентификатор сотрудника
		telegram_id: Telegram id сотрудника
		fullname: ФИО сотрудника
		username: Никнейм телеграм
	"""
	__tablename__ = 'Employee'

	employee_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	fullname = Column(String, nullable=False)
	username = Column(String)

	role = relationship('EmployeeRole', back_populates='employee')

	def __str__(self):
		return f'{self.employee_id} {self.telegram_id} {self.fullname} {self.role_id}'


class EmployeeRole(Base):
	"""
	Роли сотрудников.

	У одного сотрудника может быть несколько ролей.

	Колонки:
		employee_id: Сотрудник
		role_id: Роль
	"""
	__tablename__ = 'EmployeeRole'

	employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
	role_id = Column(Integer, ForeignKey('Role.role_id'), nullable=False)

	employee = relationship('Employee', back_populates='role')
	about_role = relationship('Role', back_populates='employee')

	__table_args__ = (
		PrimaryKeyConstraint(employee_id, role_id),
	)

	def __str__(self):
		return f'{self.employee_id} {self.role_id}'


class RegistrationRequest(Base):
	"""
	Запросы на регистрацию.

	Колонки:
		request_id: Идентификатор запроса
		telegram_id: Telegram id
		from_name: ФИО, которое пользователь указал при регистрации
		from_username: Никнейм Telegram,
		roles: Идентификаторы роли сотрудника; строка 'role_id1,role_id2 ...'
	"""
	__tablename__ = 'RegistrationRequest'

	request_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False)
	from_name = Column(String, nullable=False)
	from_username = Column(VARCHAR(50), nullable=False)
	roles = Column(String, nullable=False)

	def __str__(self):
		return f'{self.request_id} {self.telegram_id} {self.from_name} {self.from_username}'


class Class(Base):
	"""
	Классы.

	Колонки:
		class_id: Идентификатор класса
		class_name: Имя класса ('7А', '10Б' ...)
		last_date: Когда последний раз был отмечен класс
	"""
	__tablename__ = 'Class'

	class_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	class_name = Column(VARCHAR(10), unique=True)
	last_date = Column(Date)

	student_class = relationship('Student', back_populates='student')

	def __str__(self):
		return f'{self.class_id} {self.class_name} {self.last_date}'


class Student(Base):
	"""
	Ученики.

	Колонки:
		student_id: Идентификатор ученика
		surname: Фамилия
		name: Имя
		middlename [OPTIONAL]: Отчество
		class_id: Класс ученика
	"""
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
	"""
	Черный список.

	Колонки:
		blocked_user_id: Идентификатор заблокированного пользователя
		telegram_id: Telegram id
		fullname: ФИО заблокированного пользователя
		username: Имя пользователя телеграм без '@'
	"""
	__tablename__ = 'BlockedUser'

	blocked_user_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	telegram_id = Column(Integer, nullable=False, unique=True)
	fullname = Column(String)
	username = Column(String)

	def __str__(self):
		return f'{self.blocked_user_id} {self.telegram_id} {self.fullname} {self.username}'


class AbsenceReason(Base):
	"""
	Причины отсутствия.

	Колонки:
		reason_id: Идентификатор причины
		title: Название
		description: Описание
		in_lyceum: Находится ли в лицее ученик, отсутствуя по данной причине
	"""
	__tablename__ = 'AbsenceReason'

	reason_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	title = Column(VARCHAR(100), nullable=False)
	description = Column(String, nullable=False)
	in_lyceum = Column(Boolean, nullable=False)

	reason = relationship('Absent', back_populates='absent')

	def __str__(self):
		return f'{self.reason_id} {self.title} {self.description} {self.in_lyceum}'


class Absent(Base):
	"""
	Отсутствующие ученики.

	Колонки:
		absent_id: Идентификатор отсутствующего ученика
		reason_id: Причина отсутствия
		student_id: Ученик
		date: Дата отсутствия
	"""
	__tablename__ = 'Absent'

	absent_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
	reason_id = Column(Integer, ForeignKey('AbsenceReason.reason_id'), nullable=False)
	student_id = Column(Integer, ForeignKey('Student.student_id'), nullable=False)
	date = Column(Date)

	absent = relationship('AbsenceReason', back_populates='reason')
	about_student = relationship('Student', back_populates='absent_student')

	def __str__(self):
		return f'{self.absent_id} {self.reason_id} {self.student_id} {self.date}'
