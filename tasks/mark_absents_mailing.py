import datetime

import asyncio

from database import crud
from loader import bot


class Mailer:
	FIRST_APPEAL_TIME = datetime.time(hour=7, minute=50)
	SECOND_APPEAL_TIME = datetime.time(hour=8, minute=30)
	THIRD_APPEAL_TIME = datetime.time(hour=9, minute=0)

	@staticmethod
	async def first_appeal():
		for teacher in crud.table_employee.get_teachers():
			telegram_id = teacher.telegram_id
			text = "🔊 Коллеги, доброе утро! Просьба всем учителям отметить отсутствующих."
			await bot.send_message(telegram_id, text=text)

	@staticmethod
	async def second_appeal():
		not_marked_classes = crud.table_class.not_marked_classes(datetime.date.today())
		if not_marked_classes:
			for teacher in crud.table_employee.get_teachers():
				classes_by_comma = ', '.join([class_.class_name for class_ in not_marked_classes])

				text = f"Просьба всем учителям отметить отсутствующих.\n Осталось отметить: {classes_by_comma}."
				await bot.send_message(teacher.telegram_id, text)

	@staticmethod
	async def third_appeal():
		not_marked_classes = crud.table_class.not_marked_classes(datetime.date.today())
		if not_marked_classes:
			for teacher in crud.table_employee.get_teachers():
				classes_by_comma = ', '.join([class_.class_name for class_ in not_marked_classes])

				text = f"Просьба всем учителям отметить отсутствующих.\n Осталось отметить: {classes_by_comma}."
				await bot.send_message(teacher.telegram_id, text)

	async def start(self):
		while True:
			now_time = datetime.time(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute)
			if now_time == self.FIRST_APPEAL_TIME:
				await self.first_appeal()
			elif now_time == self.SECOND_APPEAL_TIME:
				await self.second_appeal()
			elif now_time == self.THIRD_APPEAL_TIME:
				await self.third_appeal()
			await asyncio.sleep(60)
