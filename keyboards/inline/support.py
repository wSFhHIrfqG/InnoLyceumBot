from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def write_support_message_markup():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton(text='✏️ Написать сообщение', callback_data='support')
	markup.add(btn)
	return markup