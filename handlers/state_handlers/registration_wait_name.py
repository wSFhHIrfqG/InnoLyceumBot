from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
import keyboards
from database import crud
from config_data import config


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.registration_wait_name)
async def register_user(message: types.Message, state=FSMContext):
	await state.set_state(UserStates.start)
	request_id = crud.table_registration_request.add_registration_request(
		telegram_id=message.from_user.id,
		from_name=message.text,
		from_username=message.from_user.username
	)

	await bot.delete_message(message.from_user.id, message.message_id)
	await bot.edit_message_text(
		text='📨 Ваша заявка отправлена и будет рассмотрена администраторами!',
		chat_id=message.from_user.id,
		message_id=message.message_id - 1,
	)

	await bot.send_message(
		chat_id=config.SUPER_ADMIN_TELEGRAM_ID,
		text=f'📩 Получена заявка на регистрацию\n\n'
			 f'<b>От:</b> {message.text}\n'
			 f'<b>Профиль:</b> @{message.from_user.username}\n'
			 f'<b>Telegram ID:</b> <code>{message.from_user.id}</code>\n\n',
		reply_markup=keyboards.inline.registration.registration_request_markup(request_id, message)
	)
