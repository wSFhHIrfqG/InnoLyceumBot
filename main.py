import asyncio

from aiogram.utils import executor

import handlers  # noqa
from loader import dp
from tasks.mark_absents_mailing import Mailer

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	mailer = Mailer()
	loop.create_task(mailer.start())
	executor.start_polling(dp)
