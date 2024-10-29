from database import db
from database import models
from config_data import roles


def get_all():
	"""Получить все данные из таблицы EmployeeRole"""
	session = db.SessionLocal()
	query = session.query(models.EmployeeRole)

	data = query.filter().all()
	return data


def get_admins():
	session = db.SessionLocal()
	query = session.query(models.EmployeeRole)
	admins = [
		employee_role.employee_id for employee_role in query.filter(
			models.EmployeeRole.role_id.in_(roles.ADMIN_ROLES)
		).group_by(
			models.EmployeeRole.employee_id
		).all()
	]
	return admins


def get_teachers():
	session = db.SessionLocal()
	query = session.query(models.EmployeeRole)
	admins = [
		employee_role.employee_id for employee_role in query.filter(
			models.EmployeeRole.role_id.in_(roles.TEACHER_ROLES)
		).group_by(
			models.EmployeeRole.employee_id
		).all()
	]
	return admins


def get_employees():
	session = db.SessionLocal()
	query = session.query(models.EmployeeRole)
	admins = [
		employee_role.employee_id for employee_role in query.filter(
			models.EmployeeRole.role_id.in_(roles.EMPLOYEE_ROLES)
		).group_by(
			models.EmployeeRole.employee_id
		).all()
	]
	return admins


def set_employee_role(employee_id: int, role_id: int):
	session = db.SessionLocal()
	employee_role = models.EmployeeRole(
		employee_id=employee_id,
		role_id=role_id
	)
	session.add(employee_role)
	session.commit()


def get_employee_roles(employee_id: int):
	session = db.SessionLocal()
	query = session.query(models.EmployeeRole)
	return query.filter(models.EmployeeRole.employee_id == employee_id).all()
