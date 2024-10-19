from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config_data import roles
from database import crud


def start_markup(telegram_id: int):
	employee_roles = [
		role.role_id for role in crud.table_employee.get_employee_by_telegram_id(telegram_id)
	]

	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	for role_id in employee_roles:
		if role_id in roles.ADMIN_ROLES:
			markup.row(KeyboardButton(text='⚙️ Администрирование'))
		if role_id in roles.TEACHER_ROLES:
			markup.row(KeyboardButton(text='🖍 Отметить отсутствующих'))
		if role_id in roles.EMPLOYEE_ROLES:
			pass
	return markup
