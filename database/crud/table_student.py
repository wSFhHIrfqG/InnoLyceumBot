from database import db
from database import models
from database import crud
import utils


def get_all():
	"""Получить все данные из таблицы Student"""
	session = db.SessionLocal()
	query = session.query(models.Student)

	data = query.filter().all()
	return data


def load_students():
	session = db.SessionLocal()
	session.query(models.Student).delete()  # Очищаем таблицу
	session.commit()

	try:
		for student in utils.parse_students.iter_students():
			student_initials = student.fullname.split()
			surname = student_initials[0]
			name = student_initials[1]
			middlename = None
			if len(student_initials) > 2:
				middlename = student_initials[2]

			class_name = student.class_name
			class_id = crud.table_class.add_class(class_name=class_name)

			add_student(surname=surname, name=name, middlename=middlename, class_id=class_id)
	except FileNotFoundError:
		return False
	else:
		return True


def add_student(surname: str, name: str, middlename: str | None, class_id: int):
	session = db.SessionLocal()
	student = models.Student(
		surname=surname,
		name=name,
		middlename=middlename,
		class_id=class_id
	)
	session.add(student)
	session.commit()


def get_students_by_class(class_id: int):
	session = db.SessionLocal()
	query = session.query(models.Student)
	return query.filter(models.Student.class_id == class_id).all()


def count_students_by_class(class_id: int):
	session = db.SessionLocal()
	query = session.query(models.Student)
	return query.filter(models.Student.class_id == class_id).count()


def get_student(student_id: int):
	session = db.SessionLocal()
	query = session.query(models.Student)
	return query.filter(models.Student.student_id == student_id).one_or_none()


def count_all_students():
	session = db.SessionLocal()
	return session.query(models.Student).count()
