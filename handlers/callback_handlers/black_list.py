from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import dp, bot
from states.user_states import UserStates
from database import crud
import keyboards


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
		await bot.send_message(
			chat_id=call.from_user.id,
			text='Выберите действие',
			reply_markup=keyboards.reply.admin.admin_markup()
		)
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
	await call.message.delete()
	await state.set_state(UserStates.admin_menu)
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Выберите действие',
		reply_markup=keyboards.reply.admin.admin_markup()
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='bl_close')
async def bl_close(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
