from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.reply.admin
from loader import dp, bot
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='mailing_cancel', state=UserStates.admin_mailing_wait_message)
async def mailing_cancel(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Отменено')
	await state.set_state(UserStates.admin_menu)
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Выберите действие',
		reply_markup=keyboards.reply.admin.admin_markup()
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='mailing_cancel', state='*')
async def mailing_cancel(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Отменено')
