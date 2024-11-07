from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def employees_markup(employees: list):
	markup = InlineKeyboardMarkup()

	for employee in employees:
		btn = InlineKeyboardButton(
			text=f'{employee.fullname}',
			callback_data=f'show_employee:{employee.employee_id}'
		)
		markup.row(btn)

	close_btn = InlineKeyboardButton('❌ Закрыть', callback_data='employees_close')
	markup.row(close_btn)
	return markup


def edit_employee_markup(employee_id: int):
	markup = InlineKeyboardMarkup()

	to_employees_btn = InlineKeyboardButton(
			text='⬅️ К сотрудникам', callback_data='to_employees'
	)
	delete_employee_btn = InlineKeyboardButton(
		text='Удалить', callback_data=f'delete_employee:{employee_id}'
	)

	markup.row(delete_employee_btn)
	markup.row(to_employees_btn)
	return markup
