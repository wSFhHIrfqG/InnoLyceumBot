from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from database import crud
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='start_registration', state='*')
async def send_registration_request(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete_reply_markup()

	if crud.table_registration_request.get_request_by_telegram_id(call.from_user.id):
		await call.message.reply('🚫 Вы уже отправили заявку на регистрацию!')
	else:
		await bot.send_message(
			call.from_user.id,
			'Введите <b>ФИО</b> через пробел без дополнительных символов\n\n'
			'<b>Например:</b> Иванов Максим Игоревич'
		)
		await state.set_state(UserStates.registration_wait_name)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='registration_request_accept', state='*')
async def accept_registration_request(call: types.CallbackQuery, state: FSMContext):
	request_id, request_sender_telegram_id = map(int, call.data.split(':')[1:])
	await call.message.delete_reply_markup()
	crud.table_registration_request.close_registration_request(request_id)
	await call.message.reply('Запрос одобрен. Не забудьте добавить пользователя в таблицу, '
							 'если еще не сделали этого и обновить данные в панели администратора.')
	await bot.send_message(
		request_sender_telegram_id,
		'✅ Ваш запрос на регистрацию одобрен!\n\n'
		'⚠️ Если вы еще не получили доступ ко всем функциям бота,'
		'вероятно администраторы пока не добавили вас в базу. Попробуйте позже.'
	)
	crud.table_employee.load_employees()  # Подгружаем новых сотрудников


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='registration_request_cancel', state='*')
async def cancel_registration_request(call: types.CallbackQuery, state: FSMContext):
	request_id, request_sender_telegram_id = map(int, call.data.split(':')[1:])
	await call.message.delete_reply_markup()
	crud.table_registration_request.close_registration_request(request_id)
	await call.message.reply('Запрос отклонен')
	await call.message.reply('Добавить пользователя в черный список?',
							 reply_markup=keyboards.inline.registration.confirm_user_blocking(
								 request_sender_telegram_id))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='blocking_user_accept', state='*')
async def block_user(call: types.CallbackQuery, state: FSMContext):
	user_telegram_id = int(call.data.split(':')[1])
	crud.table_blocked_user.block_user(user_telegram_id)
	await bot.delete_message(call.from_user.id, call.message.message_id)
	await call.message.reply_to_message.reply('🔏 Позьзователь заблокирован')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='blocking_user_cancel', state='*')
async def do_nothing(call: types.CallbackQuery, state: FSMContext):
	await bot.delete_message(call.from_user.id, call.message.message_id)
