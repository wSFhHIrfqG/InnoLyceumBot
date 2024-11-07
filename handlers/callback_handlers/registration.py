from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import bot, dp
from states.user_states import UserStates
from config_data import config
from database import crud
import keyboards


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text='start_registration',
	state='*')
async def ask_name(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()

	if not data.get('registration'):
		await state.update_data({'registration': dict()})

	# Если запрос от данного telegram_id уже есть или пользователь уже добавлен
	if crud.table_registration_request.get_request_by_telegram_id(call.from_user.id) \
			or crud.table_employee.get_employee_by_telegram_id(call.from_user.id):
		await call.message.edit_text(text='Вы уже отправили заявку на регистрацию')
	else:
		text = 'Введите <b>ФИО</b> через пробел без дополнительных символов.\n' \
			   '<b>Например:</b> Иванов Максим Игоревич'
		await call.message.edit_text(text=text)
		await state.set_state(UserStates.registration_wait_name)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text_startswith='registration_role_chosen',
	state='*')
async def remember_role_choice(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id
	role_id = int(call.data.split(':')[1])

	data = await state.get_data()
	msg_registration_data = data.get('registration', {}).get(message_id, {})
	roles_chosen = msg_registration_data.get('roles_chosen')
	if roles_chosen is None:
		roles_chosen = set()

	if role_id in roles_chosen:
		roles_chosen.remove(role_id)
	else:
		roles_chosen.add(role_id)

	msg_registration_data['roles_chosen'] = roles_chosen
	data['registration'][message_id] = msg_registration_data
	await state.update_data(data=data)

	roles = crud.table_role.get_all()
	await call.message.edit_reply_markup(
		reply_markup=keyboards.inline.registration.roles_markup(roles, roles_chosen)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text='role_choice_complete',
	state='*')
async def send_request(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id
	data = await state.get_data()
	msg_registration_data = data.get('registration', {}).get(message_id)

	# telegram_id
	telegram_id = call.from_user.id

	# from_name
	from_name = msg_registration_data.get('from_name')

	# from_username
	from_username = call.from_user.username

	# roles_chosen
	roles_chosen = msg_registration_data.get('roles_chosen', [])

	# Если запрос от данного telegram_id уже есть или пользователь уже добавлен
	if crud.table_registration_request.get_request_by_telegram_id(telegram_id) \
			or crud.table_employee.get_employee_by_telegram_id(telegram_id):
		registration_data = data.get('registration', {})
		registration_data.pop(message_id, None)
		if len(registration_data):
			data['registration'] = registration_data
		else:
			data.pop('registration', None)
		await state.update_data(data=data)

		await call.message.delete_reply_markup()
		await bot.send_message(
			chat_id=telegram_id,
			text='Вы уже отправили заявку на регистрацию'
		)
		return

	roles_id_string = ','.join(str(role_id) for role_id in roles_chosen)
	request_id = crud.table_registration_request.add_registration_request(
		telegram_id=telegram_id,
		from_name=from_name,
		from_username=from_username,
		roles=roles_id_string
	)

	roles = []
	for role_id in roles_chosen:
		role = crud.table_role.get_role(role_id)
		roles.append(role)

	pretty_roles_string = ', '.join(role.title for role in roles)
	await bot.send_message(
		config.SUPER_ADMIN_TELEGRAM_ID,
		text=f'📩 Получена заявка на регистрацию\n\n'
			 f'<b>ФИО:</b> {from_name}\n'
			 f'<b>Должности:</b> {pretty_roles_string}\n'
			 f'<b>Telegram ID:</b> <code>{telegram_id}</code>\n'
			 f'<b>Профиль:</b> @{from_username}\n\n',
		reply_markup=keyboards.inline.registration.registration_request_markup(request_id)
	)

	await call.message.delete_reply_markup()
	await bot.send_message(
		telegram_id,
		text='📨 Ваша заявка отправлена и будет рассмотрена администраторами\n\n'
			 f'<b>ФИО:</b> {from_name}\n'
			 f'<b>Должности:</b> {pretty_roles_string}'
	)

	registration_data = data.get('registration', {})
	registration_data.pop(message_id, None)
	if len(registration_data):
		data['registration'] = registration_data
	else:
		data.pop('registration', None)
	await state.update_data(data=data)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text_startswith='registration_request_accept',
	state='*')
async def accept_registration_request(call: types.CallbackQuery, state: FSMContext):
	request_id = int(call.data.split(':')[1])
	request = crud.table_registration_request.get_registration_request(request_id)
	telegram_id = request.telegram_id
	fullname = request.from_name
	username = request.from_username
	roles = map(int, request.roles.split(','))

	employee_id = crud.table_employee.add_employee(
		telegram_id=telegram_id, fullname=fullname, username=username)
	for role_id in roles:
		crud.table_employee_role.set_employee_role(
			employee_id=employee_id, role_id=role_id)

	crud.table_registration_request.close_registration_request(request_id)
	await call.message.delete_reply_markup()
	await call.message.reply('Сотрудник добавлен')

	await bot.send_message(
		chat_id=request.telegram_id,
		text='Ваш запрос на регистрацию одобрен'
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text_startswith='registration_request_cancel',
	state='*')
async def cancel_registration_request(call: types.CallbackQuery, state: FSMContext):
	request_id = int(call.data.split(':')[1])

	await call.message.delete_reply_markup()
	await call.message.reply('Запрос отклонен')
	await call.message.reply(
		text='Добавить пользователя в черный список?',
		reply_markup=keyboards.inline.registration.confirm_user_blocking(request_id)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text_startswith='blocking_user_accept',
	state='*')
async def blocking_user_accept(call: types.CallbackQuery, state: FSMContext):
	request_id = int(call.data.split(':')[1])
	request = crud.table_registration_request.get_registration_request(request_id)

	crud.table_blocked_user.block_user(
		telegram_id=request.telegram_id,
		fullname=request.from_name,
		username=request.from_username
	)
	crud.table_registration_request.close_registration_request(request_id)

	await call.message.edit_text('🔏 Пользователь заблокирован')

	await bot.send_message(
		chat_id=request.telegram_id,
		text='Ваш запрос на регистрацию отклонен'
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	text_startswith='blocking_user_cancel',
	state='*')
async def blocking_user_cancel(call: types.CallbackQuery, state: FSMContext):
	request_id = int(call.data.split(':')[1])
	request = crud.table_registration_request.get_registration_request(request_id)

	crud.table_registration_request.close_registration_request(request_id)

	await bot.delete_message(call.from_user.id, call.message.message_id)

	await bot.send_message(
		chat_id=request.telegram_id,
		text='Ваш запрос на регистрацию отклонен'
	)
