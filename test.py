import os
import requests
import logging 
import telegram
import time 


from logging.handlers import RotatingFileHandler 
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError


timestamp = 1549962000
load_dotenv()

PRACTICUM_TOKEN=os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID=os.getenv('TELEGRAM_CHAT_ID')



RETRY_PERIOD = 600
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def get_api_answer(timestamp):
    try:
        ENDPOINT = os.getenv('ENDPOINT')
        
        response=requests.get(url=ENDPOINT, headers=HEADERS, params={'from_date':timestamp})
    except Exception:
        logger.excepptio
    return response.json()

print(get_api_answer(timestamp))