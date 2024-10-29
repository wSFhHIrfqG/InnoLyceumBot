from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message


def registration_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('👤 Регистрация', callback_data='start_registration')
	markup.add(btn)
	return markup


def roles_markup(roles: list, roles_chosen: set):
	markup = InlineKeyboardMarkup()
	for role in roles:
		if role.role_id in roles_chosen:
			btn = InlineKeyboardButton(f'✔️ {role.title}', callback_data=f'registration_role_chosen:{role.role_id}')
		else:
			btn = InlineKeyboardButton(f'{role.title}', callback_data=f'registration_role_chosen:{role.role_id}')
		markup.row(btn)

	if len(roles_chosen) >= 1:
		complete_btn = InlineKeyboardButton('✅ Готово', callback_data='role_choice_complete')
		markup.row(complete_btn)
	return markup


def registration_request_markup(request_id: int):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton('✅ Принять',
								callback_data=f'registration_request_accept:{request_id}')
	btn2 = InlineKeyboardButton('⛔️ Отклонить',
								callback_data=f'registration_request_cancel:{request_id}')
	markup.row(btn1)
	markup.row(btn2)
	return markup


def confirm_user_blocking(telegram_id: int):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton('Да', callback_data=f'blocking_user_accept:{telegram_id}')
	btn2 = InlineKeyboardButton('Нет', callback_data=f'blocking_user_cancel:{telegram_id}')
	markup.row(btn1, btn2)
	return markup
