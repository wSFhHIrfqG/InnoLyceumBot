from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы role"""
	session = db.SessionLocal()
	query = session.query(models.Role)

	data = query.filter().all()
	return data


def add_employee_roles():
	"""
	Добавить все роли для сотрудников в таблицу role.
	Используется один раз при запуске.
	При использовании таблица со старыми ролями ОЧИЩАЕТСЯ.
	"""
	session = db.SessionLocal()
	roles = [
		models.Role(role_id=1, title='Директор', description='Директор'),
		models.Role(role_id=2, title='Администратор', description='Административный работник'),
		models.Role(role_id=3, title='Учитель', description='Учитель'),
		models.Role(role_id=5, title='Сотрудник', description='Другие сотрудники лицея')
	]
	session.query(models.Role).delete()  # Очищаем таблицу
	session.add_all(roles)  # Загружаем роли
	session.commit()
