from database import db
from database import models
from database import crud
import utils
from config_data import roles
from bot_logging import logger


def get_all():
	"""Получить все данные из таблицы Employee"""
	session = db.SessionLocal()
	query = session.query(models.Employee)

	data = query.filter().all()
	return data


def load_employees():
	"""
	Записать в таблицу Employee данные из excel таблицы с сотрудниками

	:return: True, если данные успешно обновлены
	"""
	session = db.SessionLocal()
	session.query(models.Employee).delete()  # Очищаем таблицу
	session.commit()

	try:
		for employee in utils.parse_employees.iter_employees():
			role = crud.table_role.get_role_by_title(employee.role)

			if role is not None:
				surname, name, middlename = employee.fullname.split()
				add_employee(
					telegram_id=employee.telegram_id,
					surname=surname,
					name=name,
					middlename=middlename,
					role_id=role.role_id
				)
			else:
				msg = 'Сотрудник не был добавлен. Неизвестная роль: "%s" {fullname}' % employee.role
				logger.error(msg)

	except FileNotFoundError:
		return False
	else:
		return True


def add_employee(telegram_id: int, surname: str, name: str, middlename: str, role_id: int):
	session = db.SessionLocal()
	role = models.Employee(
		telegram_id=telegram_id,
		surname=surname,
		name=name,
		middlename=middlename,
		role_id=role_id
	)
	session.add(role)
	session.commit()


def get_employee_by_telegram_id(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return query.filter(models.Employee.telegram_id == telegram_id).all()


def get_teachers():
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return query.filter(models.Employee.role_id.in_(roles.TEACHER_ROLES)).all()


def get_admins():
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return query.filter(models.Employee.role_id.in_(roles.ADMIN_ROLES)).all()
