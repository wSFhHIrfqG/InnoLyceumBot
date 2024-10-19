import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
	exit('Добавьте файл .env')
else:
	load_dotenv()

TOKEN = os.getenv('TOKEN')
SUPER_ADMIN_TELEGRAM_ID = int(os.getenv('SUPER_ADMIN_TELEGRAM_ID'))

base_dir = os.path.dirname(os.path.dirname(__file__))
DATABASE_URL = 'sqlite:///' + os.path.join(base_dir, 'database', os.getenv('DATABASE_NAME'))

EMPLOYEE_DATA_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('EMPLOYEE_DATA_FILENAME'))
STUDENT_DATA_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('STUDENT_DATA_FILENAME'))
ABSENT_REPORT_TEMPLATE_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('ABSENT_REPORT_TEMPLATE'))

OUTPUT_ABSENT_REPORTS_DIR = os.path.join(base_dir, 'output', 'absence_reports')
