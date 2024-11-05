from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text='❌ Отмена', callback_data='support_cancel')
	markup.row(btn)
	return markup