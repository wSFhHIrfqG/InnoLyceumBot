from loader import bot
from config_data.commands import COMMANDS


async def set_commands(dp):
	await bot.set_my_commands(COMMANDS)
