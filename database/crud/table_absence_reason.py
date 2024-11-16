from config_data.absence_reasons import ABSENCE_REASONS
from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы AbsenceReason"""
	session = db.SessionLocal()
	query = session.query(models.AbsenceReason)

	data = query.filter().all()
	return data


def load_reasons():
	"""
	Добавить причины отсутствия в таблицу AbsenceReason.
	Используется один раз при запуске.
	При использовании таблица со старыми причинами ОЧИЩАЕТСЯ.
	"""
	session = db.SessionLocal()
	session.query(models.AbsenceReason).delete()  # Очищаем таблицу

	for reason in ABSENCE_REASONS:  # Загружаем причины
		session.add(models.AbsenceReason(**reason))

	session.commit()


def get_reason(reason_id: int):
	session = db.SessionLocal()
	query = session.query(models.AbsenceReason)
	return query.filter(models.AbsenceReason.reason_id == reason_id).one_or_none()
