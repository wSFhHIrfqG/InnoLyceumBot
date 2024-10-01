from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types

from loader import dp
from database import crud


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='load_employees', state='*')
async def load_employees(call: types.CallbackQuery, state: FSMContext):
	crud.table_employee.load_employees()
	await call.message.reply('Данные сотрудников в базе обновлены!')


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='load_students', state='*')
async def load_students(call: types.CallbackQuery, state: FSMContext):
	crud.table_student.load_students()
	await call.message.reply('Данные учеников в базе обновлены')
