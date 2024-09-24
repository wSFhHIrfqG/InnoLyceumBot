from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import dp
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['start'], state='*')
async def start(message: types.Message, state=FSMContext):
	if crud.table_employee.get_employee_by_telegram_id(message.from_user.id):
		await message.answer('Бот перезапущен')
	else:
		await message.answer('👋 Приветствую Вас в официальном боте ГАОУ "Лицей Иннополис"')
		await message.answer('Перед началом работы Вам нужно отправить заявку на регистрацию.')
