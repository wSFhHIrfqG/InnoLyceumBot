from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text='❌ Отмена', callback_data='mailing_cancel')
	markup.add(btn)
	return markup
