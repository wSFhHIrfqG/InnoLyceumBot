from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config_data import config
import database
from database.db import engine
from filters.user_registered import UserRegisteredFilter

bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создаем таблицы в бд
database.models.Base.metadata.create_all(bind=engine)

# Добавляем роли сотрудников в таблицу бд
database.crud.table_role.load_employee_roles()

# Добавляем причины отсутствия в бд
database.crud.table_absence_reason.load_reasons()

# Загружаем учеников и классы в бд
database.crud.table_student.load_students()

# Загружаем кастомные фильтры
dp.filters_factory.bind(UserRegisteredFilter)
