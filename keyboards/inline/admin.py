from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text='Загрузить учеников', callback_data='load_students')
	markup.row(btn)
	return markup
