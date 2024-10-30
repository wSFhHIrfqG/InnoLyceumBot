from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы BlockedUser"""
	session = db.SessionLocal()
	query = session.query(models.BlockedUser)

	data = query.filter().all()
	return data


def block_user(telegram_id: int, fullname: str = None, username: str = None):
	session = db.SessionLocal()

	if user_blocked(telegram_id):
		query = session.query(models.BlockedUser)
		query.filter(
			models.BlockedUser.telegram_id == telegram_id
		).update(
			{models.BlockedUser.fullname: fullname,
			 models.BlockedUser.username: username}
		)
	else:
		user = models.BlockedUser(
			telegram_id=telegram_id,
			fullname=fullname,
			username=username
		)
		session.add(user)
	session.commit()


def unlock_user(blocked_user_id: int):
	session = db.SessionLocal()
	session.query(
		models.BlockedUser
	).filter(
		models.BlockedUser.blocked_user_id == blocked_user_id
	).delete()

	# Переиндексирование пользователей
	users = session.query(models.BlockedUser).order_by(models.BlockedUser.blocked_user_id).all()

	for index, user in enumerate(users, start=1):
		user.blocked_user_id = index
		session.add(user)

	session.commit()


def user_blocked(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.BlockedUser)
	blocked_user = query.filter(models.BlockedUser.telegram_id == telegram_id).one_or_none()
	return bool(blocked_user)
