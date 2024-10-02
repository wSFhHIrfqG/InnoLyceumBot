from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	start = State()  # Бот запущен
	registration_wait_name = State()  # Пользователь вводит ФИО при регистрации
	main_menu = State()  # Начальное меню
