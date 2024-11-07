from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.inline.edit_employees
from loader import dp, bot
from states.user_states import UserStates
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='show_employee', state='*')
async def show_employee(call: types.CallbackQuery, state: FSMContext):
	employee_id = int(call.data.split(':')[1])
	employee = crud.table_employee.get_employee(employee_id)

	employee_roles_id = crud.table_employee_role.get_employee_roles(employee_id)

	roles = []
	for role_id in employee_roles_id:
		role = crud.table_role.get_role(role_id)
		roles.append(role)
	pretty_roles_string = ', '.join(role.title for role in roles)

	text = f'<b>Идентификатор:</b> <code>{employee_id}</code>\n\n' \
		   f'<b>ФИО:</b> {employee.fullname}\n' \
		   f'<b>Должности:</b> {pretty_roles_string}\n' \
		   f'<b>Telegram ID:</b> <code>{employee.telegram_id}</code>\n' \
		   f'<b>Профиль:</b> @{employee.username}'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.edit_employees.edit_employee_markup(employee_id)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text_startswith='delete_employee', state='*')
async def delete_employee(call: types.CallbackQuery, state: FSMContext):
	employee_id = int(call.data.split(':')[1])

	employee = crud.table_employee.get_employee(employee_id)
	employee_telegram_id = employee.telegram_id

	crud.table_employee.delete_employee(employee_id)
	crud.table_employee_role.delete_employee_roles(employee_id)

	employees = crud.table_employee.get_all()

	if len(employees):
		text = 'Список сотрудников'
	else:
		text = 'Список сотрудников пуст'

	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.edit_employees.employees_markup(employees)
	)

	await bot.send_message(
		chat_id=employee_telegram_id,
		text='Администраторы удалили вас из списка сотрудников'
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='to_employees', state='*')
async def to_employees(call: types.CallbackQuery, state: FSMContext):
	employees = crud.table_employee.get_all()
	if len(employees):
		text = 'Список сотрудников',
	else:
		text = 'Список сотрудников пуст'

	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.edit_employees.employees_markup(employees)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='employees_close', state=UserStates.admin_menu)
async def employees_close(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await state.set_state(UserStates.admin_menu)
	await bot.send_message(
		chat_id=call.from_user.id,
		text='Выберите действие',
		reply_markup=keyboards.reply.admin.admin_markup()
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
						   text='employees_close', state='*')
async def employees_close(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
