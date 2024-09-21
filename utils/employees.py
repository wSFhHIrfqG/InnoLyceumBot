from collections import namedtuple

import openpyxl

from config_data import config


def iter_employees():
	book = openpyxl.load_workbook(config.EMPLOYEE_DATA_FILE_PATH, read_only=True)
	sheet = book.active

	EmployeeRow = namedtuple('EmployeeRow', ['fullname', 'role', 'telegram_id'])
	for row in map(EmployeeRow._make, sheet.iter_rows(min_row=2, values_only=True)):
		yield row


def get_employee_role_number(employee):
	roles = {
		1: ['Директор', ],
		2: ['Заместитель директора', ],
		3: ['Учитель', ],
		4: ['Заведующий библиотекой', ]
	}
	for number, roles in roles.items():
		if employee.role in roles:
			return number
