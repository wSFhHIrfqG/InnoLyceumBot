from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы Employee"""
	session = db.SessionLocal()
	query = session.query(models.Employee)

	data = query.filter().all()
	return data


def add_employee(telegram_id: int, fullname: str, username: str):
	session = db.SessionLocal()
	employee = models.Employee(
		telegram_id=telegram_id,
		fullname=fullname,
		username=username
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


def get_all_unique_telegram_id():
	session = db.SessionLocal()
	query = session.query(models.Employee)
	return [
		row.telegram_id for row in
		query.group_by(models.Employee.telegram_id).all()
	]


def delete_employee(employee_id: int):
	session = db.SessionLocal()
	query = session.query(models.Employee)
	query.filter(models.Employee.employee_id == employee_id).delete()
	session.commit()
	session.close()
