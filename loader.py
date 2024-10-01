from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from config_data import config
import database
from database.db import engine

bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создаем таблицы в бд
database.models.Base.metadata.create_all(bind=engine)

# Добавляем роли сотрудников в таблицу бд
database.crud.table_role.add_employee_roles()

# Загружаем сотрудников в бд
database.crud.table_employee.load_employees()

# Добавляем учеников и классы в бд
database.crud.table_student.load_students()
