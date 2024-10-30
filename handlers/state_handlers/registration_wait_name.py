from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
import keyboards
from database import crud


@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=['text'],
					state=UserStates.registration_wait_name)
async def ask_role(message: types.Message, state=FSMContext):
	await state.set_state(UserStates.start)

	roles = crud.table_role.get_all()
	await message.delete()
	msg = await bot.send_message(
		message.from_user.id,
		text='Выберите Вашу должность (можно несколько)',
		reply_markup=keyboards.inline.registration.roles_markup(roles, roles_chosen=set())
	)

	data = await state.get_data()
	registration_data = data.get('registration', {})
	registration_data[msg.message_id] = {'from_name': message.text, 'roles_chosen': set()}
	data['registration'] = registration_data
	await state.update_data(data=data)
