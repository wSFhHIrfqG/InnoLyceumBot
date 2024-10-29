from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

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
