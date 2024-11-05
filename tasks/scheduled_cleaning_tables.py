import asyncio

from database import crud
from bot_logging import logger


class Cleaner:
	INTERVAL_IN_SECONDS = 60 * 60 * 24 * 7  # Одна неделя

	@staticmethod
	async def clean_table_absent():
		crud.table_absent.clean_table()

	async def start(self):
		while True:
			logger.info('Очищаем таблицу Absent')
			try:
				await self.clean_table_absent()
			except Exception as exc:
				logger.exception('Ошибка при очистке таблицы Absent')
				raise exc
			else:
				logger.info('Таблица Absent очищена')
			await asyncio.sleep(self.INTERVAL_IN_SECONDS)
