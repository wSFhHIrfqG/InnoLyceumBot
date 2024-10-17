from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def classes_markup(classes: list):
	markup = InlineKeyboardMarkup()
	row_width = 4
	row = []
	for class_ in classes:
		btn = InlineKeyboardButton(class_.class_name, callback_data=f'class:{class_.class_id}')
		if len(row) >= row_width:
			markup.row(*row)
			row.clear()
		row.append(btn)
	markup.row(*row)
	cancel_btn = InlineKeyboardButton(f'❌ Отмена', callback_data='mark_absents_cancel')
	markup.row(cancel_btn)
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

	to_classes_btn = InlineKeyboardButton(f'⬅ К классам', callback_data='to_classes')
	cancel_btn = InlineKeyboardButton(f'❌ Отмена', callback_data='mark_absents_cancel')
	done_btn = InlineKeyboardButton(f'✅ Готово', callback_data='mark_absents_complete')
	markup.row(to_classes_btn, cancel_btn, done_btn)
	return markup


def reasons_markup(reasons: list):
	markup = InlineKeyboardMarkup()
	for reason in reasons:
		btn = InlineKeyboardButton(reason.title, callback_data=f'reason:{reason.reason_id}')
		markup.row(btn)
	to_students_btn = InlineKeyboardButton(f'⬅ К ученикам', callback_data='to_students')
	cancel_btn = InlineKeyboardButton(f'❌ Отмена', callback_data='mark_absents_cancel')
	markup.row(to_students_btn, cancel_btn)
	return markup
