from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards
from loader import bot, dp
from states.user_states import UserStates


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	commands=['support'],
	state='*')
async def support(message: types.Message, state=FSMContext):
	await state.set_state(UserStates.support_wait_message)
	await bot.send_message(
		chat_id=message.from_user.id,
		text='Введите текст обращения',
		reply_markup=keyboards.reply.support.cancel_markup()
	)


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=False,
	commands=['support'],
	state='*')
async def support_not_allowed(message: types.Message, state=FSMContext):
	await bot.send_message(
		chat_id=message.from_user.id,
		text='Для начала нужно зарегистрироваться'
	)
