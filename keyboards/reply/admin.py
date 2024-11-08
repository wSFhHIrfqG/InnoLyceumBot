from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_markup():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = KeyboardButton(text='📃 Сотрудники')
	btn2 = KeyboardButton(text='📤 Выгрузить сотрудников')
	btn3 = KeyboardButton(text='📥 Загрузить учеников')
	btn4 = KeyboardButton(text='📓 Черный список')
	btn5 = KeyboardButton(text='📢 Рассылка')
	btn6 = KeyboardButton(text='Главное меню')
	markup.row(btn1, btn2, btn3)
	markup.row(btn4, btn5)
	markup.row(btn6)
	return markup
