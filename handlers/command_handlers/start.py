from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards
from config_data.commands import COMMANDS
from database import crud
from loader import bot, dp
from states.user_states import UserStates


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	commands=['start'],
	state='*')
async def start(message: types.Message, state=FSMContext):
	await state.set_state(UserStates.start)
	if crud.table_employee.get_employee_by_telegram_id(message.from_user.id):
		await state.set_state(UserStates.main_menu)
		await bot.send_message(message.from_user.id, 'Вы в главном меню',
							   reply_markup=keyboards.reply.start.start_markup(message.from_user.id))
	elif crud.table_registration_request.get_request_by_telegram_id(message.from_user.id):
		await bot.send_message(message.from_user.id, 'Ваша заявка на регистрацию пока не одобрена. Попробуйте позже')
	elif crud.table_blocked_user.user_blocked(message.from_user.id):
		await bot.send_message(message.from_user.id, '🙅‍♂️ Администраторы добавили вас в черный список')
	else:
		commands = '\n'.join([f'{command.command} - {command.description}' for command in COMMANDS])
		text = '👋 Приветствую Вас в официальном боте ГАОУ "Лицей Иннополис"!\n\n' \
			   '<b>Команды:</b>\n' \
			   f'{commands}\n\n' \
			   'Перед началом работы Вам нужно отправить заявку на регистрацию.'
		await bot.send_message(
			chat_id=message.from_user.id,
			text=text,
			reply_markup=keyboards.inline.registration.registration_markup()
		)
