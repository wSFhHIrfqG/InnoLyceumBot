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


def load_students_and_classes():
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
