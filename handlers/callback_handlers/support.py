from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.inline.support
from loader import bot, dp
from states.user_states import UserStates


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='support', state='*')
async def support(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.support_wait_message)

	await call.message.delete()
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Введите текст',
		reply_markup=keyboards.inline.support.cancel_markup()
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='support_cancel', state='*')
async def support_cancel(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Отменено')

	await state.set_state(UserStates.main_menu)
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Вы в главном меню',
		reply_markup=keyboards.reply.start.start_markup(call.from_user.id)
	)
