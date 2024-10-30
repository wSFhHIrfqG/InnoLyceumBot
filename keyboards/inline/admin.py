from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_markup():
	markup = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(text='Выгрузить сотрудников', callback_data='export_employees')
	btn2 = InlineKeyboardButton(text='Загрузить учеников', callback_data='load_students')
	btn3 = InlineKeyboardButton(text='Черный список', callback_data='black_list')
	markup.row(btn1)
	markup.row(btn2)
	markup.row(btn3)
	return markup
