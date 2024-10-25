from database import db
from database import models


def get_all():
	session = db.SessionLocal()
	query = session.query(models.RegistrationRequest)

	data = query.filter().all()
	return data


def add_registration_request(telegram_id: int, from_name: str, from_username: str):
	session = db.SessionLocal()
	registration_request = models.RegistrationRequest(
		telegram_id=telegram_id,
		from_name=from_name,
		from_username=from_username
	)
	session.add(registration_request)
	session.commit()
	return registration_request.request_id


def close_registration_request(request_id: int):
	session = db.SessionLocal()
	query = session.query(models.RegistrationRequest)
	query.filter(models.RegistrationRequest.request_id == request_id).delete()
	session.commit()


def get_request_by_telegram_id(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.RegistrationRequest)
	return query.filter(models.RegistrationRequest.telegram_id == telegram_id).all()
