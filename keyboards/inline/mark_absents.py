from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def classes_markup(classes: list):
	markup = InlineKeyboardMarkup()
	for class_ in classes:
		btn = InlineKeyboardButton(class_.class_name, callback_data=f'class:{class_.class_id}')
		markup.row(btn)
	return markup


def students_markup(students: list, absents: list):
	markup = InlineKeyboardMarkup()

	absent_students_id = [absent.get('student_id') for absent in absents]  # student_id отсутствующих
	for student in students:
		if student.student_id in absent_students_id:
			btn = InlineKeyboardButton(f'⭕️ {student.surname} {student.name}',
									   callback_data=f'student:{student.student_id}')
		else:
			btn = InlineKeyboardButton(f'⚪️ {student.surname} {student.name}',
									   callback_data=f'student:{student.student_id}')
		markup.row(btn)
	return markup


def reasons_markup(reasons: list):
	markup = InlineKeyboardMarkup()
	for reason in reasons:
		btn = InlineKeyboardButton(reason.title, callback_data=f'reason:{reason.reason_id}')
		markup.row(btn)
	return markup
