from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.reply.admin
from loader import dp, bot
from states.user_states import UserStates


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state=UserStates.admin_mailing_wait_message,
	text='mailing_cancel')
async def mailing_cancel(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(
		text='Отменено',
		reply_markup=keyboards.reply.admin.admin_markup()
	)
	await state.set_state(UserStates.admin_menu)
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Выберите действие'
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='mailing_cancel')
async def mailing_cancel(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Отменено')
