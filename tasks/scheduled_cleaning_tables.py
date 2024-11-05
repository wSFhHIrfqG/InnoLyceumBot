import asyncio
import datetime
from datetime import time

from database import crud
from bot_logging import logger


class Cleaner:
	WEEKDAY = 0  # День недели, когда очищается таблица
	TIME = time(hour=4, minute=0)  # Время
	INTERVAL_IN_SECONDS = 60 * 60 * 24 * 7  # Интервал

	@staticmethod
	async def clean_table_absent():
		crud.table_absent.clean_table()

	async def start(self):
		while True:
			now = datetime.datetime.now()
			now_time = datetime.time(hour=now.hour, minute=now.minute)

			if (now.weekday() == self.WEEKDAY) and (now_time == self.TIME):
				logger.info('Очищаем таблицу Absent')
				try:
					await self.clean_table_absent()
				except Exception as exc:
					logger.exception('Ошибка при очистке таблицы Absent')
					raise exc
				else:
					logger.info('Таблица Absent очищена')
				await asyncio.sleep(self.INTERVAL_IN_SECONDS)
			else:
				await asyncio.sleep(60)

