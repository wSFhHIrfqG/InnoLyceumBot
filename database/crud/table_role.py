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
	roles = [
		models.Role(role_id=1, title='Директор', description='Директор лицея'),
		models.Role(role_id=2, title='Заместитель директора', description='Заместитель директора'),
		models.Role(role_id=3, title='Учитель', description='Учитель'),
		models.Role(role_id=4, title='Заведующий библиотекой', description='Заведующий библиотекой')
	]
	session.query(models.Role).delete()  # Очищаем таблицу
	session.add_all(roles)  # Загружаем роли
	session.commit()


def get_role_by_title(title: str):
	session = db.SessionLocal()
	query = session.query(models.Role)
	return query.filter(models.Role.title == title).one_or_none()
