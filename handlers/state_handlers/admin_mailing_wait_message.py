from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.message_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	content_types=['text'],
	state=UserStates.admin_mailing_wait_message)
async def mail_message(message: types.Message, state=FSMContext):
	if message.text == '❌ Отмена':
		await bot.send_message(
			chat_id=message.from_user.id,
			text='Отменено'
		)
	else:
		for telegram_id in crud.table_employee.get_all_unique_telegram_id():
			if telegram_id == message.from_user.id:
				continue

			text = '📢 <b>Рассылка</b>\n\n' \
				   f'{message.text}'
			await bot.send_message(
				chat_id=telegram_id,
				text=text
			)
		await message.reply(text='Сообщение отправлено')

	await state.set_state(UserStates.admin_menu)
	await bot.send_message(
		chat_id=message.from_user.id,
		text='Выберите действие',
		reply_markup=keyboards.reply.admin.admin_markup()
	)
