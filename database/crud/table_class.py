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
