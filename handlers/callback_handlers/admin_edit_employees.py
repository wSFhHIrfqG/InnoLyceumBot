from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards.inline.edit_employees
from database import crud
from loader import dp, bot
from states.user_states import UserStates


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='show_employee')
async def show_employee(call: types.CallbackQuery, state: FSMContext):
	employee_id = int(call.data.split(':')[1])
	employee = crud.table_employee.get_employee(employee_id)

	employee_roles_id = crud.table_employee_role.get_employee_roles(employee_id)

	username = employee.username
	pretty_username = 'Не известен' if username is None else f'@{username}'

	roles = []
	for role_id in employee_roles_id:
		role = crud.table_role.get_role(role_id)
		roles.append(role)
	pretty_roles_string = ', '.join(role.title for role in roles)

	text = f'<b>ФИО:</b> {employee.fullname}\n' \
		   f'<b>Должности:</b> {pretty_roles_string}\n' \
		   f'<b>Telegram ID:</b> <code>{employee.telegram_id}</code>\n' \
		   f'<b>Профиль:</b> {pretty_username}'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.edit_employees.edit_employee_markup(employee_id)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='delete_employee')
async def delete_employee(call: types.CallbackQuery, state: FSMContext):
	employee_id = int(call.data.split(':')[1])

	employee = crud.table_employee.get_employee(employee_id)
	employee_telegram_id = employee.telegram_id

	crud.table_employee.delete_employee(employee_id)
	crud.table_employee_role.delete_employee_roles(employee_id)

	employees = crud.table_employee.get_all()
	if len(employees):
		text = 'Список сотрудников'
		await call.message.edit_text(
			text=text,
			reply_markup=keyboards.inline.edit_employees.employees_markup(employees)
		)
	else:
		text = 'Список сотрудников пуст'
		await call.message.edit_text(text=text)

	await bot.send_message(
		chat_id=employee_telegram_id,
		text='Администраторы удалили вас из списка сотрудников',
		reply_markup=types.ReplyKeyboardRemove()
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='to_employees')
async def to_employees(call: types.CallbackQuery, state: FSMContext):
	employees = crud.table_employee.get_all()
	if len(employees):
		text = 'Список сотрудников'
		await call.message.edit_text(
			text=text,
			reply_markup=keyboards.inline.edit_employees.employees_markup(employees)
		)
	else:
		text = 'Список сотрудников пуст'
		await call.message.edit_text(text=text)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state=UserStates.admin_menu,
	text='employees_close')
async def employees_close(call: types.CallbackQuery, state: FSMContext):
	await state.set_state(UserStates.admin_menu)
	await call.message.edit_text(text='Список скрыт')


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='employees_close')
async def employees_close(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text(text='Список скрыт')
