from collections import namedtuple

import openpyxl

from config_data import config


def iter_students():
	book = openpyxl.load_workbook(config.STUDENT_DATA_FILE_PATH, read_only=True)
	sheet = book.active

	StudentRow = namedtuple('StudentRow', ['fullname', 'class_name'])
	for row in map(StudentRow._make, sheet.iter_rows(min_row=2, values_only=True)):
		yield row

	book.close()
