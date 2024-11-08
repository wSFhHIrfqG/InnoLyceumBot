import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
	exit('Добавьте файл .env')
else:
	load_dotenv()

TOKEN = os.getenv('TOKEN')
SUPER_ADMIN_TELEGRAM_ID = int(os.getenv('SUPER_ADMIN_TELEGRAM_ID'))
DEVELOPER_TELEGRAM_ID = int(os.getenv('DEVELOPER_TELEGRAM_ID'))

GROUP_ID = os.getenv('GROUP_ID')  # Optional key
if GROUP_ID is not None:
	GROUP_ID = int(GROUP_ID)

base_dir = os.path.dirname(os.path.dirname(__file__))
DATABASE_URL = 'sqlite:///' + os.path.join(base_dir, 'database', os.getenv('DATABASE_NAME'))

STUDENT_DATA_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('STUDENT_DATA_FILENAME'))
ABSENT_REPORT_TEMPLATE_FILE_PATH = os.path.join(base_dir, 'input', os.getenv('ABSENT_REPORT_TEMPLATE_FILENAME'))

OUTPUT_ABSENT_REPORTS_DIR = os.path.join(base_dir, 'output', 'absence_reports')
OUTPUT_EMPLOYEES_DIR = os.path.join(base_dir, 'output', 'employees')
