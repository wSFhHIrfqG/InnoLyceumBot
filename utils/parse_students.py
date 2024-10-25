from collections import namedtuple

import openpyxl

from config_data import config
from bot_logging import logger


def iter_students():
	book = None
	try:
		book = openpyxl.load_workbook(config.STUDENT_DATA_FILE_PATH, read_only=True)
	except FileNotFoundError as exc:
		msg = 'Файл %s c данными об учениках не найден. ' \
			  'Убедитесь, что тот существует и находится в папке input. ' \
			  'Проверьте имя файла в переменных окружения.' % config.STUDENT_DATA_FILE_PATH
		logger.exception(msg)
		raise exc
	else:
		sheet = book.active

		StudentRow = namedtuple('StudentRow', ['fullname', 'class_name'])
		for row in map(StudentRow._make, sheet.iter_rows(min_row=2, values_only=True)):
			yield row
	finally:
		if book:
			book.close()
