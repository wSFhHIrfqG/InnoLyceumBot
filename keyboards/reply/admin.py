from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_markup():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = KeyboardButton(text='📤 Выгрузить сотрудников')
	btn2 = KeyboardButton(text='📥 Загрузить учеников')
	btn3 = KeyboardButton(text='📓 Черный список')
	btn4 = KeyboardButton(text='📢 Рассылка')
	btn5 = KeyboardButton(text='Главное меню')
	markup.row(btn1, btn2)
	markup.row(btn3, btn4)
	markup.row(btn5)
	return markup
