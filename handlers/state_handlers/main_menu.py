from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import datetime

from loader import bot, dp
from states.user_states import UserStates
from config_data import roles
from database import crud
import keyboards


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	content_types=['text'],
	state=UserStates.main_menu)
async def action_chosen(message: types.Message, state=FSMContext):
	employee = crud.table_employee.get_employee_by_telegram_id(message.from_user.id)
	employee_roles = crud.table_employee_role.get_employee_roles(employee.employee_id)

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

	if is_admin:
		if message.text == '⚙️ Администрирование':
			await state.set_state(UserStates.admin_menu)
			await bot.send_message(
				chat_id=message.from_user.id, text='Выберите действие',
				reply_markup=keyboards.reply.admin.admin_markup()
			)

	if is_teacher:
		if message.text == '🖍 Отметить отсутствующих':
			not_marked_classes_today = crud.table_class.not_marked_classes(date=datetime.date.today())
			if not not_marked_classes_today:
				await bot.send_message(
					chat_id=message.from_user.id, text='За сегодня все классы уже отмечены'
				)
			else:
				await bot.send_message(
					chat_id=message.from_user.id, text='Выберите класс',
					reply_markup=keyboards.inline.mark_absents.classes_markup(not_marked_classes_today)
				)

	elif is_employee:
		pass
