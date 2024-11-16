from sqlalchemy import func

from config_data.roles import ROLES
from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы Role"""
	session = db.SessionLocal()
	query = session.query(models.Role)

	data = query.filter().all()
	return data


def load_employee_roles():
	"""
	Добавить все роли для сотрудников в таблицу role.
	Используется один раз при запуске.
	При использовании таблица со старыми ролями ОЧИЩАЕТСЯ.
	"""
	session = db.SessionLocal()
	session.query(models.Role).delete()  # Очищаем таблицу

	for role in ROLES:  # Загружаем роли
		session.add(models.Role(**role))

	session.commit()


def get_role_by_title(title: str):
	session = db.SessionLocal()
	query = session.query(models.Role)
	return query.filter(func.lower(models.Role.title) == func.lower(title)).one_or_none()


def get_role(role_id: int):
	session = db.SessionLocal()
	query = session.query(models.Role)
	return query.filter(models.Role.role_id == role_id).one_or_none()
