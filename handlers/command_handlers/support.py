from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['support'], state='*')
async def support(message: types.Message, state=FSMContext):
	if crud.table_employee.get_employee_by_telegram_id(telegram_id=message.from_user.id):
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Здесь вы можете оставить свои идеи и предложения',
			reply_markup=keyboards.inline.support.write_support_message_markup()
		)
	else:
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Вы не зарегистрированы'
		)
