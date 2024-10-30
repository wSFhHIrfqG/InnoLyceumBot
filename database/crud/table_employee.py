from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы Employee"""
	session = db.SessionLocal()
	query = session.query(models.Employee)

	data = query.filter().all()
	return data


def add_employee(telegram_id: int, fullname: str):
	session = db.SessionLocal()
	employee = models.Employee(
		telegram_id=telegram_id,
		fullname=fullname
	)
	session.add(employee)
	session.commit()
	return employee.employee_id


def get_employee_by_telegram_id(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return query.filter(models.Employee.telegram_id == telegram_id).one_or_none()


def get_employee(employee_id: int):
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return query.filter(models.Employee.employee_id == employee_id).one_or_none()
