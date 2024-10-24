import datetime
import os

from docxtpl import DocxTemplate
from docx.opc.exceptions import PackageNotFoundError

from bot_logging import logger
from database import crud
from config_data import config


def create_report(date: datetime.date):
	date_s = datetime.date.strftime(date, '%d.%m.%Y')

	doc = DocxTemplate(config.ABSENT_REPORT_TEMPLATE_FILE_PATH)

	context = {}
	class_prefix = {
		'7А': 'a_7', '7Б': 'b_7',
		'8А': 'a_8', '8Б': 'b_8',
		'9А': 'a_9', '9Б': 'b_9',
		'10А': 'a_10', '10Б': 'b_10',
		'11А': 'a_11', '11Б': 'b_11',
	}
	context['date'] = date_s

	all_students = 0
	all_in_lyceum = 0
	for class_ in crud.table_class.marked_classes(datetime.date.today()):
		prefix = class_prefix.get(class_.class_name)

		students_in_class = crud.table_student.count_students_by_class(class_.class_id)  # Учеников в классе
		absent_students = 0  # Отсутствующие
		absent_in = 0  # В лицее
		absent_out = 0  # Вне лицея

		all_in_lyceum += students_in_class
		all_students += students_in_class

		absents = []
		for absent in crud.table_absent.absents_in_class(class_.class_id, datetime.date.today()):
			absent_students += 1

			absence_reason = crud.table_absence_reason.get_reason(absent.reason_id)
			if absence_reason.in_lyceum:
				absent_in += 1
			else:
				absent_out += 1
				all_in_lyceum -= 1

			student = crud.table_student.get_student(absent.student_id)

			absents.append(f'{student.surname} {student.name} ({absence_reason.title})')

		context[prefix] = students_in_class - absent_students  # Учеников присутствует
		context[prefix + '_in'] = absent_in
		context[prefix + '_out'] = absent_out
		context[prefix + '_all'] = students_in_class
		context[prefix + '_absent'] = ', '.join(absents)

	context['all_in_lyceum'] = all_in_lyceum
	context['all_students'] = all_students

	try:
		doc.render(context)
	except PackageNotFoundError as exc:
		logger.error(
			'Файл с шаблоном отчёта об отсутствующих не найден. '
			'Убедитесь, что тот существует и находится в папке input'
		)
		logger.exception(exc)
		raise exc

	output_dir = config.OUTPUT_ABSENT_REPORTS_DIR
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	fp = os.path.join(output_dir, f'{date_s}.docx')
	doc.save(fp)
	return fp


if __name__ == '__main__':
	create_report(datetime.date.today())
