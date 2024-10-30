from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.inline.support
from loader import bot, dp
from states.user_states import UserStates
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='support', state='*')
async def support(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

	if crud.table_employee.get_employee_by_telegram_id(telegram_id=call.from_user.id):
		await state.set_state(UserStates.support_wait_message)

		await bot.send_message(
			chat_id=call.from_user.id,
			text='Введите текст',
			reply_markup=keyboards.reply.support.cancel_markup()
		)
	else:
		await bot.send_message(
			chat_id=call.from_user.id,
			text='Вы не зарегистрированы'
		)
