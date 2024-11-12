import datetime

from database import crud


def handle_absent_data():
	data = {
		'all_students': 0,
		'all_in_lyceum': 0
	}

	for class_ in crud.table_class.marked_classes(datetime.date.today()):
		data[class_.class_id] = {
			'students_in_class': crud.table_student.count_students_by_class(class_.class_id),
			'absent_students': 0,
			'absent_in': 0,
			'absent_out': 0,
			'absents_name_reason': []
		}

		data['all_in_lyceum'] += data[class_.class_id].get('students_in_class', 0)
		data['all_students'] += data[class_.class_id].get('students_in_class', 0)

		for absent in crud.table_absent.absents_in_class(class_.class_id, datetime.date.today()):
			data[class_.class_id]['absent_students'] += 1

			student = crud.table_student.get_student(absent.student_id)
			reason = crud.table_absence_reason.get_reason(absent.reason_id)
			data[class_.class_id]['absents_name_reason'].append(
				f'{student.surname} {student.name} ({reason.title})'
			)

			absence_reason = crud.table_absence_reason.get_reason(absent.reason_id)
			if absence_reason.in_lyceum:
				data[class_.class_id]['absent_in'] += 1
			else:
				data[class_.class_id]['absent_out'] += 1
				data['all_in_lyceum'] -= 1

	return data
