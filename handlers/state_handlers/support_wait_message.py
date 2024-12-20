from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards.reply.start
from config_data import config
from loader import bot, dp
from states.user_states import UserStates


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	content_types=['text'],
	state=UserStates.support_wait_message)
async def send_support_message(message: types.Message, state=FSMContext):
	if message.text == '❌ Отмена':
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Отменено',
			reply_markup=keyboards.reply.start.start_markup(message.from_user.id)
		)
	else:
		support_message = message.text

		await state.set_state(UserStates.main_menu)

		text_to_admins = f'📬 Получено новое сообщение\n\n' \
						 f'<b>Текст:</b> {support_message}'

		await bot.send_message(chat_id=config.DEVELOPER_TELEGRAM_ID, text=text_to_admins)

		await message.reply(
			text='Ваше сообщение отправлено',
			reply_markup=keyboards.reply.start.start_markup(message.from_user.id)
		)

	await state.set_state(UserStates.main_menu)
