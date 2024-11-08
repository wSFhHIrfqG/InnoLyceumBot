from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from database import crud


class UserRegisteredFilter(BoundFilter):
	key = "user_registered"

	def __init__(self, user_registered: bool):
		self.user_registered = user_registered

	async def check(self, message: types.Message) -> bool:
		user = crud.table_employee.get_employee_by_telegram_id(message.from_user.id)
		return self.user_registered == (user is not None)
