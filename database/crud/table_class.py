from sqlalchemy import func
import datetime

from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы Class"""
	session = db.SessionLocal()
	query = session.query(models.Class)

	data = query.filter().all()
	return data


def add_class(class_name: str):
	session = db.SessionLocal()
	query = session.query(models.Class)
	existing_class = query.filter(models.Class.class_name == class_name).one_or_none()
	if not existing_class:
		class_ = models.Class(class_name=class_name)
		session.add(class_)
		session.commit()
		return class_.class_id
	else:
		return existing_class.class_id


def get_class(class_id: int):
	session = db.SessionLocal()
	query = session.query(models.Class)
	return query.filter(models.Class.class_id == class_id).one_or_none()


def not_marked_classes(date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Class)
	return query.filter(
		(models.Class.last_date.is_(None)) | (func.date(models.Class.last_date) < date)
	).all()


def marked_classes(date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Class)
	return query.filter(func.date(models.Class.last_date) == date).all()


def set_last_date(class_id: int, date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Class)
	query.filter(models.Class.class_id == class_id).update({models.Class.last_date: date})
	session.commit()
