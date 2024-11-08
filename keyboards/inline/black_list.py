from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def black_list_markup(i: int, n: int):
	markup = InlineKeyboardMarkup()

	unlock_user_btn = InlineKeyboardButton(text='Разблокировать', callback_data=f'unlock_user:{i}')
	close_btn = InlineKeyboardButton(text='Закрыть', callback_data='bl_close')
	empty_btn = InlineKeyboardButton(text=' ', callback_data='ignore')

	# Пролистать на 5 влево или пустая кнопка
	if i - 5 >= 0:
		hard_left_btn = InlineKeyboardButton(text='⋘', callback_data=f'bl_hard_left:{i}')
	else:
		hard_left_btn = empty_btn

	# Пролистать на 1 влево или пустая кнопка
	if i - 1 >= 0:
		left_btn = InlineKeyboardButton(text='⪻', callback_data=f'bl_left:{i}')
	else:
		left_btn = empty_btn

	# Пролистать на 1 вправо или пустая кнопка
	if i + 1 < n:
		right_btn = InlineKeyboardButton(text='⪼', callback_data=f'bl_right:{i}')
	else:
		right_btn = empty_btn

	# Пролистать на 5 вправо или пустая кнопка
	if i + 5 < n:
		hard_right_btn = InlineKeyboardButton(text='⋙', callback_data=f'bl_hard_right:{i}')
	else:
		hard_right_btn = empty_btn

	if n != 1:
		markup.row(hard_left_btn, left_btn, right_btn, hard_right_btn)
	markup.row(unlock_user_btn)
	markup.row(close_btn)

	return markup
