from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import datetime

from loader import dp
from database import crud
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='class', state='*')
async def choose_absents(call: types.CallbackQuery, state: FSMContext):
	class_id = int(call.data.split(':')[1])
	await state.update_data(dict(class_id=class_id))
	class_students = crud.table_student.get_students_by_class(class_id)
	absents_in_class = crud.table_absent.absents_in_class(class_id, date=datetime.date.today())
	await call.message.edit_text(text='Выберите отсутствующих',
								 reply_markup=keyboards.inline.mark_absents.students_markup(
									 class_students, absents_in_class)
								 )


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='student', state='*')
async def choose_reason(call: types.CallbackQuery, state: FSMContext):
	student_id = int(call.data.split(':')[1])
	data = await state.get_data()
	class_id = data.get('class_id')
	await state.update_data(dict(student_id=student_id))
	absent = crud.table_absent.get_absent(student_id, datetime.date.today())
	if absent is not None:
		crud.table_absent.delete_absent(absent.absent_id)
		class_students = crud.table_student.get_students_by_class(class_id)
		absents_in_class = crud.table_absent.absents_in_class(class_id, date=datetime.date.today())
		await call.message.edit_reply_markup(reply_markup=keyboards.inline.mark_absents.students_markup(
			class_students, absents_in_class))
	else:
		await call.message.edit_text(text='Выберите причину отсутствия',
									 reply_markup=keyboards.inline.mark_absents.reasons_markup(
										 crud.table_absence_reason.get_all()))


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='reason', state='*')
async def save_absent(call: types.CallbackQuery, state: FSMContext):
	reason_id = int(call.data.split(':')[1])
	data = await state.get_data()
	class_id = data.get('class_id')
	crud.table_absent.add_absent(reason_id=reason_id, student_id=data.get('student_id'),
								 date=datetime.date.today())
	class_students = crud.table_student.get_students_by_class(data.get('class_id'))
	absents_in_class = crud.table_absent.absents_in_class(class_id, date=datetime.date.today())
	await call.message.edit_text(text='Выберите отсутствующих',
								 reply_markup=keyboards.inline.mark_absents.students_markup(
									 class_students, absents_in_class))
