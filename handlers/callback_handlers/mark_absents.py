import datetime

from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.utils.exceptions import ChatNotFound
from docx.opc.exceptions import PackageNotFoundError

from loader import dp, bot, logger
from config_data import config
from database import crud
import keyboards
from utils.create_absence_report import create_report


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='class', state='*')
async def choose_absents(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id
	class_id = int(call.data.split(':')[1])

	data = await state.get_data()
	if data.get(call.message.message_id):
		message_data = data.get(message_id)
	else:
		message_data = dict()

	message_data['class_id'] = class_id
	message_data['absents'] = message_data['absents'] if message_data.get('absents') else dict()
	message_data['absents'][class_id] = list()
	await state.update_data(class_id=class_id)
	await state.update_data({message_id: message_data})

	absents = message_data.get('absents', {})
	absents_in_class = absents.get(class_id, [])

	class_ = crud.table_class.get_class(class_id)
	if class_.last_date == datetime.date.today():
		not_marked_classes_today = crud.table_class.not_marked_classes(date=datetime.date.today())
		await call.message.edit_reply_markup(
			reply_markup=keyboards.inline.mark_absents.classes_markup(not_marked_classes_today))
	else:
		class_students = crud.table_student.get_students_by_class(class_id)
		await call.message.edit_text(
			text='Выберите отсутствующих',
			reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
		)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='student', state='*')
async def choose_reason(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id
	student_id = int(call.data.split(':')[1])

	data = await state.get_data()
	message_data = data.get(message_id)
	class_id = message_data.get('class_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])

	absent_students_id = [absent.get('student_id') for absent in absents_in_class]  # student_id отсутствующих
	if student_id in absent_students_id:
		# Убираем ученика из отсутствующих
		absents_in_class = [absent for absent in absents_in_class if absent.get('student_id') != student_id]
		message_data['absents'][class_id] = absents_in_class
		await state.update_data({message_id: message_data})

		class_students = crud.table_student.get_students_by_class(class_id)
		await call.message.edit_reply_markup(
			reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
		)
	else:
		message_data['student_id'] = student_id
		await state.update_data({message_id: message_data})
		await call.message.edit_text(
			text='Выберите причину отсутствия',
			reply_markup=keyboards.inline.mark_absents.reasons_markup(crud.table_absence_reason.get_all())
		)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text_startswith='reason', state='*')
async def save_absent(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id
	reason_id = int(call.data.split(':')[1])

	data = await state.get_data()
	message_data = data.get(message_id)
	class_id = message_data.get('class_id')
	student_id = message_data.get('student_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])

	# Запоминаем отсутствующего
	message_data['absents'][class_id].append(
		{'reason_id': reason_id, 'student_id': student_id}
	)
	await state.update_data({message_id: message_data})

	class_students = crud.table_student.get_students_by_class(class_id)
	await call.message.edit_text(
		text='Выберите отсутствующих',
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='to_classes', state='*')
async def to_classes(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	message_data = data.get(message_id)
	class_id = message_data.pop('class_id', None)
	message_data['absents'].pop(class_id, None)
	await state.update_data({message_id: message_data})

	not_marked_classes_today = crud.table_class.not_marked_classes(date=datetime.date.today())
	await call.message.edit_text(
		text='Выберите класс',
		reply_markup=keyboards.inline.mark_absents.classes_markup(not_marked_classes_today)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='to_students', state='*')
async def to_students(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	message_data = data.get(message_id)
	message_data.pop('student_id', None)
	class_id = message_data.get('class_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])
	await state.update_data({message_id: message_data})

	class_students = crud.table_student.get_students_by_class(data.get('class_id'))
	await call.message.edit_text(
		text='Выберите отсутствующих',
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='mark_absents_complete',
						   state='*')
async def mark_absents_complete(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	message_data = data.get(message_id)
	class_id = message_data.get('class_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])
	data.pop(message_id, None)
	await state.update_data(data=data)

	class_ = crud.table_class.get_class(class_id)
	if class_.last_date == datetime.date.today():
		await call.message.edit_text(f'{class_.class_name} класс уже был отмечен ранее')
	else:
		crud.table_class.set_last_date(class_id=class_id, date=datetime.date.today())

		for absent_dict in absents_in_class:
			crud.table_absent.add_absent(
				reason_id=absent_dict.get('reason_id'),
				student_id=absent_dict.get('student_id'),
				date=datetime.date.today()
			)

		await call.message.edit_text(f'Вы успешно отметили {class_.class_name} класс!')

		if not crud.table_class.not_marked_classes(datetime.date.today()):
			for admin in crud.table_employee.get_admins():
				try:
					try:
						report_file_path = create_report(datetime.date.today())  # Создаем отчет
					except PackageNotFoundError:  # Не найден шаблон отчета
						return
					else:  # Отправляем отчет админам
						with open(report_file_path, 'rb') as file:
							await bot.send_document(admin.telegram_id, document=file, caption='Все классы отмечены')
				except ChatNotFound:  # Чат админа не найден
					logger.warning(
						f'Отчет не был отправлен: чат админа не найден '
						f'{{'
						f'employee_id: {admin.employee_id}, '
						f'telegram_id: {admin.telegram_id}, '
						f'fullname: {admin.name} {admin.surname} {admin.middlename}'
						f'}}'
					)


@dp.callback_query_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), text='mark_absents_cancel', state='*')
async def mark_absents_cancel(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	data.pop(message_id, None)
	await state.update_data(data=data)

	await call.message.edit_text('Отменено')
