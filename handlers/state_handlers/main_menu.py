from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import datetime

from loader import bot, dp
from states.user_states import UserStates
from config_data import roles
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.main_menu)
async def action_chosen(message: types.Message, state=FSMContext):
	user_roles = [
		role.role_id for role in crud.table_employee.get_employee_by_telegram_id(message.from_user.id)
	]

	for user_role in user_roles:
		if user_role in roles.ADMIN_ROLES:
			if message.text == '⚙️ Администрирование':
				await bot.send_message(message.from_user.id, 'Выберите действие',
									   reply_markup=keyboards.inline.admin.admin_markup())

		if user_role in roles.TEACHER_ROLES:
			if message.text == '🖍 Отметить отсутствующих':
				not_marked_classes_today = crud.table_class.not_marked_classes(date=datetime.date.today())
				if not not_marked_classes_today:
					await bot.send_message(
						message.from_user.id,
						'За сегодня все классы уже отмечены'
					)
				else:
					await bot.send_message(
						message.from_user.id,
						'Выберите класс',
						reply_markup=keyboards.inline.mark_absents.classes_markup(not_marked_classes_today)
					)

		elif user_role in roles.EMPLOYEE_ROLES:
			pass
