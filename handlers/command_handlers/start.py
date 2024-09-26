from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from config_data import config
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	if message.from_user.id == config.SUPER_ADMIN_TELEGRAM_ID:
		await bot.send_message(message.from_user.id, 'Стартовое сообщение для SuperAdmin')
	elif crud.table_employee.get_employee_by_telegram_id(message.from_user.id):
		await bot.send_message(message.from_user.id, 'Бот перезапущен')
	elif crud.table_registration_request.get_request_by_telegram_id(message.from_user.id):
		await bot.send_message(message.from_user.id, '⏱ Ваша заявка на регистрацию пока не одобрена. Попробуйте позже.')
	else:
		await bot.send_message(
			message.from_user.id,
			'👋 Приветствую Вас в официальном боте ГАОУ "Лицей Иннополис"!\n'
			'Перед началом работы Вам нужно отправить заявку на регистрацию.',
			reply_markup=keyboards.inline.registration.registration_markup()
		)
