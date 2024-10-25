from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_markup():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text='Обновить сотрудников', callback_data='load_employees')
	btn2 = InlineKeyboardButton(text='Обновить учеников', callback_data='load_students')
	markup.row(btn1)
	markup.row(btn2)
	return markup
