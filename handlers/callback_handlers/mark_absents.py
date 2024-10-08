from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
import datetime

from loader import dp, bot
from database import crud
import keyboards


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='class', state='*')
async def choose_absents(call: types.CallbackQuery, state: FSMContext):
	class_id = int(call.data.split(':')[1])

	await state.update_data(class_id=class_id)

	data = await state.get_data()
	absents = data.get('absents', {})
	absents_in_class = absents.get(class_id, [])
	await state.update_data(absents=absents)

	class_students = crud.table_student.get_students_by_class(class_id)
	await call.message.edit_text(
		text='Выберите отсутствующих',
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='student', state='*')
async def choose_reason(call: types.CallbackQuery, state: FSMContext):
	student_id = int(call.data.split(':')[1])

	await state.update_data(student_id=student_id)
	data = await state.get_data()
	class_id = data.get('class_id')
	absents = data.get('absents', {})
	absents_in_class = absents.get(class_id, [])

	absent_students_id = [absent.get('student_id') for absent in absents_in_class]  # student_id отсутствующих
	if student_id in absent_students_id:
		absents_in_class = [absent for absent in absents_in_class if absent.get('student_id') != student_id]
		absents[class_id] = absents_in_class
		await state.update_data(absents=absents)

		class_students = crud.table_student.get_students_by_class(class_id)
		await call.message.edit_reply_markup(
			reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
		)
	else:
		await call.message.edit_text(
			text='Выберите причину отсутствия',
			reply_markup=keyboards.inline.mark_absents.reasons_markup(crud.table_absence_reason.get_all())
		)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='reason', state='*')
async def save_absent(call: types.CallbackQuery, state: FSMContext):
	reason_id = int(call.data.split(':')[1])

	data = await state.get_data()
	class_id = data.get('class_id')
	student_id = data.get('student_id')

	absents = data.get('absents', {})
	absents_in_class = absents.get(class_id, [])

	absents_in_class.append(
		{'reason_id': reason_id, 'student_id': student_id}
	)  # Запоминаем отсутствующего
	absents[class_id] = absents_in_class
	await state.update_data(absents=absents)

	class_students = crud.table_student.get_students_by_class(data.get('class_id'))
	await call.message.edit_text(
		text='Выберите отсутствующих',
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='to_classes', state='*')
async def to_classes(call: types.CallbackQuery, state: FSMContext):
	not_marked_classes_today = crud.table_class.not_marked_classes(date=datetime.date.today())
	await call.message.edit_text(
		text='Выберите класс',
		reply_markup=keyboards.inline.mark_absents.classes_markup(not_marked_classes_today)
	)
