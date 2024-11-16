from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards
from database import crud
from loader import dp
from states.user_states import UserStates


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='unlock_user')
async def unlock_user(call: types.CallbackQuery, state: FSMContext):
	i = int(call.data.split(':')[1])

	crud.table_blocked_user.unlock_user(blocked_user_id=i + 1)

	blocked_users = crud.table_blocked_user.get_all()
	n = len(blocked_users)

	if not n:
		await call.message.edit_text(text='Черный список пуст')
		return

	if i >= n:
		new_i = i - 1
		user = blocked_users[i - 1]
	else:
		new_i = i
		user = blocked_users[i]

	username = user.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	text = f'<b>Пользователь:</b> {new_i + 1} ({n})\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {pretty_username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(new_i, n)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_hard_left')
async def bl_hard_left(call: types.CallbackQuery, state: FSMContext):
	i = int(call.data.split(':')[1])

	blocked_users = crud.table_blocked_user.get_all()
	n = len(blocked_users)

	new_i = i - 5
	if new_i >= 0:
		user = blocked_users[new_i]
	else:
		new_i = i
		user = blocked_users[i]

	username = user.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	text = f'<b>Пользователь:</b> {new_i + 1} ({n})\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {pretty_username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(new_i, n)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_left')
async def bl_left(call: types.CallbackQuery, state: FSMContext):
	i = int(call.data.split(':')[1])

	blocked_users = crud.table_blocked_user.get_all()
	n = len(blocked_users)

	new_i = i - 1
	if new_i >= 0:
		user = blocked_users[new_i]
	else:
		new_i = i
		user = blocked_users[i]

	username = user.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	text = f'<b>Пользователь:</b> {new_i + 1} ({n})\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {pretty_username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(new_i, n)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_right')
async def bl_right(call: types.CallbackQuery, state: FSMContext):
	i = int(call.data.split(':')[1])

	blocked_users = crud.table_blocked_user.get_all()
	n = len(blocked_users)

	new_i = i + 1
	if new_i < n:
		user = blocked_users[new_i]
	else:
		new_i = i
		user = blocked_users[i]

	username = user.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	text = f'<b>Пользователь:</b> {new_i + 1} ({n})\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {pretty_username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(new_i, n)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_hard_right')
async def bl_hard_right(call: types.CallbackQuery, state: FSMContext):
	i = int(call.data.split(':')[1])

	blocked_users = crud.table_blocked_user.get_all()
	n = len(blocked_users)

	new_i = i + 5
	if new_i < n:
		user = blocked_users[new_i]
	else:
		new_i = i
		user = blocked_users[i]

	username = user.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	text = f'<b>Пользователь:</b> {new_i + 1} ({n})\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {pretty_username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(new_i, n)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state=UserStates.admin_menu,
	text_startswith='bl_close')
async def bl_close(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.admin_menu)
	await call.message.edit_text(text='Список скрыт')


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_close')
async def bl_close(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Список скрыт')
