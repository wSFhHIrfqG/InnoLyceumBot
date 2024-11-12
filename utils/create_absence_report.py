import datetime
import os

from docx.opc.exceptions import PackageNotFoundError
from docxtpl import DocxTemplate

from bot_logging import logger
from config_data import config
from database import crud
from utils.handle_absent_data import handle_absent_data


def create_report(date: datetime.date):
	logger.info('Формируем отчёт об отсутствующих')

	date_s = datetime.date.strftime(date, '%d.%m.%Y')
	output_dir = config.OUTPUT_ABSENT_REPORTS_DIR
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	fp = os.path.join(output_dir, f'{date_s}.docx')

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

	data = handle_absent_data()
	context['all_in_lyceum'] = data.get('all_in_lyceum')
	context['all_students'] = data.get('all_students')

	for class_ in crud.table_class.marked_classes(datetime.date.today()):
		prefix = class_prefix.get(class_.class_name)
		class_data = data.get(class_.class_id)

		context[prefix] = class_data.get('students_in_class') - class_data.get('absent_students')
		context[prefix + '_in'] = class_data.get('absent_in')
		context[prefix + '_out'] = class_data.get('absent_out')
		context[prefix + '_all'] = class_data.get('students_in_class')
		context[prefix + '_absent'] = ', '.join(class_data.get('absents_name_reason'))

	try:
		doc.render(context)
		doc.save(fp)
	except PackageNotFoundError as exc:
		msg = 'Файл с шаблоном отчёта об отсутствующих не найден. ' \
			  'Убедитесь, что тот существует и находится в папке input. ' \
			  'Проверьте имя файла в переменных окружения.'
		logger.exception(msg)
	except PermissionError:
		logger.exception(
			'Ошибка доступа при сохранении отчёта об отсутствующих.'
			'Попробуйте закрыть файл %s' % fp)
	else:
		logger.info('Отчёт об отсутствующих успешно сформирован')
		return fp


if __name__ == '__main__':
	create_report(datetime.date.today())
