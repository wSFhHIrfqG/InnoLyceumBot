from database import db
from database import models
import utils


def get_all():
	"""Получить все данные из таблицы Employee"""
	session = db.SessionLocal()
	query = session.query(models.Employee)

	data = query.filter().all()
	return data


def load_employees():
	for employee in utils.parse_employees.iter_employees():
		employee_role_number = utils.parse_employees.get_employee_role_number(employee)

		if employee_role_number is not None:
			surname, name, middlename = employee.fullname.split()
			add_employee(
				telegram_id=employee.telegram_id,
				surname=surname,
				name=name,
				middlename=middlename,
				role_id=employee_role_number
			)


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
