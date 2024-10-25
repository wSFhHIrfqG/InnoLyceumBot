from database import db
from database import models


def block_user(telegram_id: int):
	session = db.SessionLocal()
	user = models.BlockedUser(telegram_id=telegram_id)
	session.add(user)
	session.commit()


def user_blocked(telegram_id: int):
	session = db.SessionLocal()
	query = session.query(models.BlockedUser)
	blocked_user = query.filter(models.BlockedUser.telegram_id == telegram_id).one_or_none()
	return bool(blocked_user)
