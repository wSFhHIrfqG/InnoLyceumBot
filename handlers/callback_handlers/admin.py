from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

import keyboards.inline.black_list
from loader import dp, bot
from database import crud
from utils.export import export_employees


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='export_employees', state='*')
async def send_employees_document(call: types.CallbackQuery, state: FSMContext):
	file_path = export_employees()

	await call.message.delete()

	with open(file_path, 'rb') as file:
		await bot.send_document(call.from_user.id, file)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='load_students', state='*')
async def load_students(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_text('⏳ Данные обновляются')
	if crud.table_student.load_students():
		await call.message.edit_text('Данные учеников в базе обновлены')
	else:
		await call.message.edit_text('Упс... Загрузить учеников не удалось. Проверьте файл логов.')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='black_list', state='*')
async def black_list(call: types.CallbackQuery, state: FSMContext):
	blocked_users = crud.table_blocked_user.get_all()
	i = 0  # Индекс заблокированного пользователя
	n = len(blocked_users)  # Всего заблокированных пользователей

	if not n:
		await call.message.edit_text(text='Черный список пуст')
		return

	user = blocked_users[0]
	text = f'<b>Пользователь:</b> {i + 1}/{n}\n\n' \
		   f'<b>ФИО:</b> {user.fullname}\n' \
		   f'<b>Профиль:</b> {user.username}\n' \
		   f'<b>Telegram ID:</b> <code>{user.telegram_id}</code>'
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.black_list.black_list_markup(i, n)
	)
