from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_markup():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	btn = KeyboardButton('❌ Отмена')
	markup.add(btn)
	return markup
