from aiogram.utils import executor
import handlers  # noqa
from loader import dp

if __name__ == '__main__':
	executor.start_polling(dp)
