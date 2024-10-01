from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	if crud.table_employee.get_employee_by_telegram_id(message.from_user.id):
		await state.set_state(UserStates.start)
		await bot.send_message(message.from_user.id, 'Бот перезапущен',
							   reply_markup=keyboards.reply.start.start_markup(message.from_user.id))
	elif crud.table_registration_request.get_request_by_telegram_id(message.from_user.id):
		await bot.send_message(message.from_user.id, '⏱ Ваша заявка на регистрацию пока не одобрена. Попробуйте позже.')
	else:
		await bot.send_message(
			message.from_user.id,
			'👋 Приветствую Вас в официальном боте ГАОУ "Лицей Иннополис"!\n'
			'Перед началом работы Вам нужно отправить заявку на регистрацию.',
			reply_markup=keyboards.inline.registration.registration_markup()
		)
