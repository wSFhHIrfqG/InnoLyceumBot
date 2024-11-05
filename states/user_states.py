from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
	start = State()  # Бот запущен впервые
	registration_wait_name = State()  # Пользователь вводит ФИО при регистрации

	main_menu = State()  # Начальное меню

	support_wait_message = State()  # Пользователь вводит сообщение в поддержку

	admin_mailing_wait_message = State()  # Администратор вводит сообщение для рассылки
