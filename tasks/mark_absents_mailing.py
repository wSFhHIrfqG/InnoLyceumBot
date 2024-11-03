import datetime

import asyncio

from database import crud
from loader import bot


class Mailer:
	FIRST_APPEAL_TIME = datetime.time(hour=7, minute=50)
	SECOND_APPEAL_TIME = datetime.time(hour=8, minute=30)
	THIRD_APPEAL_TIME = datetime.time(hour=9, minute=0)
	SKIP_WEEKDAYS = [6]

	def __str__(self):
		return f'Mailer: {{' \
			   f'FIRST_APPEAL_TIME: {self.FIRST_APPEAL_TIME},' \
			   f'SECOND_APPEAL_TIME: {self.SECOND_APPEAL_TIME},' \
			   f'THIRD_APPEAL_TIME: {self.THIRD_APPEAL_TIME},' \
			   f'SKIP_WEEKDAYS: {self.SKIP_WEEKDAYS}' \
			   f'}}'

	@staticmethod
	async def first_appeal():
		for teacher_employee_id in crud.table_employee_role.get_teachers():
			employee = crud.table_employee.get_employee(teacher_employee_id)
			if employee:
				text = "🔊 Коллеги, доброе утро! Просьба всем учителям отметить отсутствующих."
				await bot.send_message(employee.telegram_id, text=text)

	@staticmethod
	async def second_appeal():
		not_marked_classes = crud.table_class.not_marked_classes(datetime.date.today())
		if not_marked_classes:
			for teacher_employee_id in crud.table_employee_role.get_teachers():
				employee = crud.table_employee.get_employee(teacher_employee_id)
				if employee:
					classes_by_comma = ', '.join([class_.class_name for class_ in not_marked_classes])

					text = f"Просьба всем учителям отметить отсутствующих.\n" \
						   f"Осталось отметить: {classes_by_comma}"
					await bot.send_message(employee.telegram_id, text)

	@staticmethod
	async def third_appeal():
		not_marked_classes = crud.table_class.not_marked_classes(datetime.date.today())
		if not_marked_classes:
			for teacher_employee_id in crud.table_employee_role.get_teachers():
				employee = crud.table_employee.get_employee(teacher_employee_id)
				if employee:
					classes_by_comma = ', '.join([class_.class_name for class_ in not_marked_classes])

					text = f"Просьба всем учителям отметить отсутствующих.\n" \
						   f"Осталось отметить: {classes_by_comma}"
					await bot.send_message(employee.telegram_id, text)

	async def start(self):
		while True:
			now = datetime.datetime.now()

			if now.weekday() not in self.SKIP_WEEKDAYS:
				now_time = datetime.time(hour=now.hour, minute=now.minute)
				if now_time == self.FIRST_APPEAL_TIME:
					await self.first_appeal()
				elif now_time == self.SECOND_APPEAL_TIME:
					await self.second_appeal()
				elif now_time == self.THIRD_APPEAL_TIME:
					await self.third_appeal()

			await asyncio.sleep(60)


if __name__ == '__main__':
	print(Mailer())
