from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.reply.start
from loader import bot, dp
from states.user_states import UserStates
from config_data import config


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.support_wait_message)
async def send_support_message(message: types.Message, state=FSMContext):
	support_message = message.text
	from_username = message.from_user.username

	await state.set_state(UserStates.main_menu)

	text_to_admins = f'📬 Получено новое сообщение\n\n' \
					 f'<b>От:</b> @{from_username}\n' \
					 f'<b>Текст:</b> {support_message}'

	await bot.send_message(chat_id=config.SUPER_ADMIN_TELEGRAM_ID, text=text_to_admins)
	if config.SUPER_ADMIN_TELEGRAM_ID != config.DEVELOPER_TELEGRAM_ID:
		await bot.send_message(chat_id=config.DEVELOPER_TELEGRAM_ID, text=text_to_admins)

	await message.reply(
		text='Ваше сообщение отправлено',
		reply_markup=keyboards.reply.start.start_markup(message.from_user.id)
	)

	await state.set_state(UserStates.main_menu)
	await bot.send_message(
		chat_id=message.from_user.id,
		text='Вы в главном меню',
		reply_markup=keyboards.reply.start.start_markup(message.from_user.id)
	)
