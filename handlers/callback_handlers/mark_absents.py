import datetime

import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter

import keyboards
from bot_logging import logger
from config_data import config
from database import crud
from loader import dp, bot
from utils.create_absence_report import create_report
from utils.handle_absent_data import handle_absent_data


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='class')
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
		class_students_count = crud.table_student.count_students_by_class(class_id)
		students_on_lesson_count = class_students_count - len(absents_in_class)

		text = 'Выберите отсутствующих\n' \
			   'В классе: <b>%d из %d</b>' % (students_on_lesson_count, class_students_count)
		await call.message.edit_text(
			text=text,
			reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
		)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='student')
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
		class_students_count = crud.table_student.count_students_by_class(class_id)
		students_on_lesson_count = class_students_count - len(absents_in_class)

		text = 'Выберите отсутствующих\n' \
			   'В классе: <b>%d из %d</b>' % (students_on_lesson_count, class_students_count)
		await call.message.edit_text(
			text=text,
			reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
		)
	else:
		message_data['student_id'] = student_id
		await state.update_data({message_id: message_data})
		await call.message.edit_text(
			text='Выберите причину отсутствия',
			reply_markup=keyboards.inline.mark_absents.reasons_markup(crud.table_absence_reason.get_all())
		)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text_startswith='reason')
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
	class_students_count = crud.table_student.count_students_by_class(class_id)
	students_on_lesson_count = class_students_count - len(absents_in_class)

	text = 'Выберите отсутствующих\n' \
		   'В классе: <b>%d из %d</b>' % (students_on_lesson_count, class_students_count)
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='to_classes')
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


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='to_students')
async def to_students(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	message_data = data.get(message_id)
	message_data.pop('student_id', None)
	class_id = message_data.get('class_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])
	await state.update_data({message_id: message_data})

	class_students = crud.table_student.get_students_by_class(data.get('class_id'))
	class_students_count = crud.table_student.count_students_by_class(class_id)
	students_on_lesson_count = class_students_count - len(absents_in_class)

	text = 'Выберите отсутствующих\n' \
		   'В классе: <b>%d из %d</b>' % (students_on_lesson_count, class_students_count)
	await call.message.edit_text(
		text=text,
		reply_markup=keyboards.inline.mark_absents.students_markup(class_students, absents_in_class)
	)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='mark_absents_complete')
async def mark_absents_complete(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	# Обращаемся к данным в fsm
	data = await state.get_data()
	message_data = data.get(message_id)
	class_id = message_data.get('class_id')
	absents_in_class = message_data.get('absents', {}).get(class_id, [])
	data.pop(message_id, None)
	await state.update_data(data=data)

	# Сотрудник, отметивший класс
	from_employee = crud.table_employee.get_employee_by_telegram_id(call.from_user.id)

	# Класс, который отметили
	class_ = crud.table_class.get_class(class_id)

	# Сообщаем, если класс уже был отмечен ранее
	if class_.last_date == datetime.date.today():  # Класс уже был отмечен ранее
		await call.message.edit_text(f'{class_.class_name} класс уже был отмечен ранее')
		return

	# Помечаем класс в бд, как отмеченный
	crud.table_class.set_last_date(class_id=class_id, date=datetime.date.today())

	# Классы, которые осталось отметить
	not_marked_classes = crud.table_class.not_marked_classes(datetime.date.today())

	pretty_absents_with_reason = []  # Строки: отсутствующие с причиной
	for absent_dict in absents_in_class:
		reason_id = absent_dict.get('reason_id')
		student_id = absent_dict.get('student_id')
		date = datetime.date.today()

		# Добавляем отсутствующего в бд
		crud.table_absent.add_absent(
			reason_id=reason_id,
			student_id=student_id,
			date=date
		)

		reason = crud.table_absence_reason.get_reason(reason_id)
		absent = crud.table_absent.get_absent(student_id=student_id, date=date)
		student = crud.table_student.get_student(absent.student_id)

		pretty_absents_with_reason.append(f'{student.surname} {student.name} ({reason.title})')

	await call.message.edit_text(f'Отмечен {class_.class_name} класс')

	if config.GROUP_ID is not None:
		try:  # Отправляем информацию в группу
			logger.info('Отправляем информацию по %s классу' % class_.class_name)

			all_in_class = crud.table_student.count_students_by_class(class_id)
			students_in_class = all_in_class - len(absents_in_class)
			absents_string = ', '.join(pretty_absents_with_reason)
			text = f'{from_employee.fullname} отправил(-а) информацию по <b>{class_.class_name}</b> классу\n\n' \
				   f'Учеников в классе: <b>{students_in_class} из {all_in_class}</b>'
			if students_in_class != all_in_class:  # В классе есть отсутствующие
				text += f'\n\nОтсутствующие: {absents_string}'
			await bot.send_message(chat_id=config.GROUP_ID, text=text)
		except aiogram.utils.exceptions.ChatNotFound:
			logger.exception(
				'Не удалось отправить информацию по %s классу в группу:'
				'чат не найден {group_id: %d}' %
				(class_.class_name, config.GROUP_ID)
			)
		except aiogram.utils.exceptions.BadRequest:
			logger.exception(
				'Не удалось отправить информацию по %s классу в группу:'
				'нет разрешений писать в группу {group_id: %d}' %
				(class_.class_name, config.GROUP_ID)
			)
		except aiogram.utils.exceptions.BotKicked:
			logger.exception(
				'Не удалось отправить информацию по %s классу в группу:'
				'бот исключен из группы {group_id: %d}' %
				(class_.class_name, config.GROUP_ID)
			)
		else:
			logger.info('Информация по %s классу успешно отправлена' % class_.class_name)

		if not not_marked_classes:  # Все классы отмечены
			try:  # Отправляем информацию по количеству учеников в лицее в группу
				logger.info('Отправляем информацию по количеству учеников в лицее в группу')

				data = handle_absent_data()

				text = 'Все классы отмечены\n' \
					   'Всего в лицее: <b>%d из %d</b>' % (
						   data.get('all_in_lyceum', '?'),
						   data.get('all_students', '?')
					   )
				await bot.send_message(chat_id=config.GROUP_ID, text=text)

			except aiogram.utils.exceptions.ChatNotFound:
				logger.exception(
					'Не удалось отправить информацию по количеству учеников в лицее:'
					'чат не найден')
			except aiogram.utils.exceptions.BadRequest:
				logger.exception(
					'Не удалось отправить информацию по количеству учеников в лицее:'
					'нет разрешений писать в группу')
			except aiogram.utils.exceptions.BotKicked:
				logger.exception(
					'Не удалось отправить информацию по количеству учеников в лицее:'
					'бот исключен из группы')
			else:
				logger.info('Отправлена информация по количеству учеников в лицее')

			# Формируем отчет и отправляем в чат админам
			for admin_employee_id in crud.table_employee_role.get_admins():
				admin = crud.table_employee.get_employee(employee_id=admin_employee_id)
				try:
					report_file_path = create_report(datetime.date.today())  # Создаем отчет
					with open(report_file_path, 'rb') as file:
						await bot.send_document(admin.telegram_id, document=file, caption='Все классы отмечены')
				except aiogram.utils.exceptions.ChatNotFound:  # Чат админа не найден
					logger.warning(
						'Отчет не был отправлен: чат админа не найден '
						'{employee_id: %s, telegram_id: %s, fullname: %s %s %s}' %
						(admin.employee_id, admin.telegram_id, admin.surname, admin.name, admin.middlename)
					)


@dp.callback_query_handler(
	ChatTypeFilter(chat_type=types.ChatType.PRIVATE),
	user_registered=True,
	state='*',
	text='mark_absents_cancel')
async def mark_absents_cancel(call: types.CallbackQuery, state: FSMContext):
	message_id = call.message.message_id

	data = await state.get_data()
	data.pop(message_id, None)
	await state.update_data(data=data)

	await call.message.edit_text('Отменено')
