from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards
from utils.export import export_employees


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.admin_menu)
async def admin_action_chosen(message: types.Message, state=FSMContext):
	if message.text == '📃 Сотрудники':
		employees = crud.table_employee.get_all()
		if len(employees):
			text = 'Список сотрудников',
		else:
			text = 'Список сотрудников пуст'

		await bot.send_message(
			chat_id=message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.edit_employees.employees_markup(employees)
		)

	elif message.text == '📤 Выгрузить сотрудников':
		file_path = export_employees()

		with open(file_path, 'rb') as file:
			await bot.send_document(chat_id=message.from_user.id, document=file)

		await state.set_state(UserStates.admin_menu)
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Выберите действие',
			reply_markup=keyboards.reply.admin.admin_markup()
		)

	elif message.text == '📥 Загрузить учеников':
		if crud.table_student.load_students():
			await bot.send_message(
				chat_id=message.from_user.id,
				text='Данные учеников в базе обновлены')
		else:
			await bot.send_message(
				chat_id=message.from_user.id,
				text='Упс... Загрузить учеников не удалось. Проверьте файл логов.')

		await state.set_state(UserStates.admin_menu)
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Выберите действие',
			reply_markup=keyboards.reply.admin.admin_markup()
		)

	elif message.text == '📓 Черный список':
		blocked_users = crud.table_blocked_user.get_all()
		n = len(blocked_users)  # Всего заблокированных пользователей

		if not n:
			await bot.send_message(chat_id=message.from_user.id, text='Черный список пуст')
			await state.set_state(UserStates.admin_menu)
			await bot.send_message(
				chat_id=message.from_user.id,
				text='Выберите действие',
				reply_markup=keyboards.reply.admin.admin_markup()
			)
			return

		user = blocked_users[0]
		text = f'<b>Пользователь:</b> {1}/{n}\n\n' \
			   f'<b>ФИО:</b> {user.fullname}\n' \
			   f'<b>Профиль:</b> {user.username}\n' \
			   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
		await bot.send_message(
			chat_id=message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.black_list.black_list_markup(0, n)
		)

	elif message.text == '📢 Рассылка':
		await state.set_state(UserStates.admin_mailing_wait_message)
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Введите текст обращения',
			reply_markup=keyboards.inline.admin_mailing.cancel_markup()
		)

	elif message.text == 'Главное меню':
		await state.set_state(UserStates.main_menu)
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Вы в главном меню',
			reply_markup=keyboards.reply.start.start_markup(message.from_user.id)
		)
