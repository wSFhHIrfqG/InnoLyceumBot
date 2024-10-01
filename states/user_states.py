from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	registration_wait_name = State()  # Пользователь вводит ФИО при регистрации
	start = State()  # Начальное меню
