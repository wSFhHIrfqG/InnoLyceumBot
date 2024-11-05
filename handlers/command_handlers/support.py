from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), commands=['support'], state='*')
async def support(message: types.Message, state=FSMContext):
	if crud.table_employee.get_employee_by_telegram_id(telegram_id=message.from_user.id):
		await state.set_state(UserStates.support_wait_message)

		await bot.send_message(
			chat_id=message.from_user.id,
			text='Введите текст обращения',
			reply_markup=keyboards.inline.support.cancel_markup()
		)
	else:
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Вы не зарегистрированы'
		)
