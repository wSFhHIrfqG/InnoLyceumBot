from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message


def registration_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton('👤 Регистрация', callback_data='start_registration')
	markup.add(btn)
	return markup


def registration_request_markup(request_id: int,
								message: Message):
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton('✅ Принять',
								callback_data=f'registration_request_accept:{request_id}:{message.from_user.id}')
	btn2 = InlineKeyboardButton('⛔️ Отклонить и заблокировать',
								callback_data=f'registration_request_cancel:{request_id}:{message.from_user.id}')
	markup.row(btn1)
	markup.row(btn2)
	return markup
