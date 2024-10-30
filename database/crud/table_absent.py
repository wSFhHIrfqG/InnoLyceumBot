from sqlalchemy import func
import datetime

from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы Absent"""
	session = db.SessionLocal()
	query = session.query(models.Absent)

	data = query.filter().all()
	return data


def add_absent(reason_id: int, student_id: int, date: datetime.date):
	session = db.SessionLocal()
	absent = models.Absent(
		reason_id=reason_id,
		student_id=student_id,
		date=date
	)
	session.add(absent)
	session.commit()


def is_absent(student_id: int, date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Absent)
	return bool(query.filter(
		(models.Absent.student_id == student_id) & (func.date(models.Absent.date) == date)
	).one_or_none())


def get_absent(student_id: int, date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Absent)
	return query.filter(
		(models.Absent.student_id == student_id) & (func.date(models.Absent.date) == date)
	).one_or_none()


def delete_absent(absent_id: int):
	session = db.SessionLocal()
	query = session.query(models.Absent)
	query.filter(models.Absent.absent_id == absent_id).delete()
	session.commit()


def absents_in_class(class_id: int, date: datetime.date):
	session = db.SessionLocal()
	query = session.query(models.Absent).join(models.Student)
	return query.filter(
		(models.Student.class_id == class_id) & (func.date(models.Absent.date) == date)
	).all()


def clean_table():
	session = db.SessionLocal()
	session.query(models.Absent).delete()
	session.commit()
