import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

REFERRAL_BONUS = int(os.getenv('REFERRAL_BONUS'))
DAILY_LIMIT = int(os.getenv('DAILY_LIMIT'))

MERCHANT_ID = os.getenv('MERCHANT_ID')
SECRET_WORD_1 = os.getenv('SECRET_WORD_1')
SECRET_WORD_2 = os.getenv('SECRET_WORD_2')
NOTIFICATION_URL = os.getenv('NOTIFICATION_URL')
SUCCESS_URL = os.getenv('SUCCESS_URL')
FAIL_URL = os.getenv('FAIL_URL')

FLASK_HOST = os.getenv('FLASK_HOST')
FLASK_PORT = int(os.getenv('FLASK_PORT'))
