from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config_data import roles
from database import crud


def start_markup(telegram_id: int):
	employee = crud.table_employee.get_employee_by_telegram_id(telegram_id)
	employee_roles = [
		employee_role.role_id
		for employee_role in crud.table_employee_role.get_employee_roles(employee.employee_id)
	]

	is_admin: bool = False
	is_teacher: bool = False
	is_employee: bool = False
	for role_id in employee_roles:
		if role_id in roles.ADMIN_ROLES:
			is_admin = True
		elif role_id in roles.TEACHER_ROLES:
			is_teacher = True
		elif role_id in roles.EMPLOYEE_ROLES:
			is_employee = True

	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	if is_admin:
		markup.row(KeyboardButton(text='⚙️ Администрирование'))
	if is_teacher:
		markup.row(KeyboardButton(text='🖍 Отметить отсутствующих'))
	if is_employee:
		pass
	return markup
