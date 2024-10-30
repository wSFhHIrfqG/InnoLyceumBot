import asyncio

from aiogram.utils import executor

import handlers  # noqa
from loader import dp
from tasks.mark_absents_mailing import Mailer
from tasks.scheduled_cleaning_tables import Cleaner
from utils.set_commands import set_commands

if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	mailer = Mailer()
	cleaner = Cleaner()

	loop.create_task(mailer.start())
	loop.create_task(cleaner.start())

	executor.start_polling(dp, on_startup=set_commands)
