from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
import keyboards


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.main_menu)
async def admin(message: types.Message, state=FSMContext):
	if message.text == '⚙️ Администрирование':
		await bot.send_message(message.from_user.id, '▶️ Выберите действие',
							   reply_markup=keyboards.inline.admin.admin_markup())
