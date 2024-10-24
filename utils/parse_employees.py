from collections import namedtuple

import openpyxl

from config_data import config
from bot_logging import logger


def iter_employees():
	book = None
	try:
		book = openpyxl.load_workbook(config.EMPLOYEE_DATA_FILE_PATH, read_only=True)
	except FileNotFoundError as exc:
		msg = 'Файл %s c данными о сотрудниках не найден. ' \
			  'Убедитесь, что тот существует и находится в папке input. ' \
			  'Проверьте имя файла в переменных окружения.' % config.EMPLOYEE_DATA_FILE_PATH
		logger.exception(msg)
		raise exc
	else:
		sheet = book.active

		EmployeeRow = namedtuple('EmployeeRow', ['fullname', 'role', 'telegram_id'])
		for row in map(EmployeeRow._make, sheet.iter_rows(min_row=2, values_only=True)):
			yield row
	finally:
		if book:
			book.close()
