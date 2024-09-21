import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
	exit('Добавьте файл .env')
else:
	load_dotenv()

base_dir = os.path.dirname(os.path.dirname(__file__))

TOKEN = os.getenv('TOKEN')
DATABASE_URL = 'sqlite:///' + os.path.join(base_dir, 'database', os.getenv('DATABASE_NAME'))

EMPLOYEE_DATA_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('EMPLOYEE_DATA_FILENAME'))
