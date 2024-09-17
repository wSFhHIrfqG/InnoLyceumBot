import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
	exit('Добавьте файл .env')
else:
	load_dotenv()

TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
