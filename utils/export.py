import os
import datetime

from openpyxl import Workbook

from database import crud
from config_data import config


def export_employees():
	workbook = Workbook()
	sheet = workbook.active
	sheet.title = "employee"

	data = [['ФИО', 'Должности', 'Telegram ID']]
	for employee in crud.table_employee.get_all():
		role_titles = []
		for role_id in crud.table_employee_role.get_employee_roles(employee_id=employee.employee_id):
			role = crud.table_role.get_role(role_id=role_id)
			role_titles.append(role.title)

		pretty_roles_string = ', '.join(role_titles)
		data.append([employee.fullname, pretty_roles_string, employee.telegram_id])

	for row in data:
		sheet.append(row)

	output_dir = config.OUTPUT_EMPLOYEES_DIR
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	fp = os.path.join(output_dir, f'employees_{datetime.date.today()}.xlsx')
	workbook.save(fp)
	return fp
