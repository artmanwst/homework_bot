import os
import requests
import logging
import telegram
import time


from dotenv import load_dotenv
from http import HTTPStatus

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
RETRY_TIME = 600

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RETRY_PERIOD = 600
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка токенов. Если их нет - программа останавливается."""
    if not all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        logger.critical('Токены не найдены')
        raise KeyError()
    return (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Сообщение отправлено')
    except Exception:
        logger.error('Ошибка не удалось отправить сообщение')


def get_api_answer(timestamp):
    """Получаем результат запроса к API."""
    ENDPOINT = os.getenv('ENDPOINT')
    try:
        homeworks = requests.get(url=ENDPOINT, headers=HEADERS,
                                 params={'from_date': timestamp})
        homework_status = homeworks.status_code
    except Exception as error:
        raise KeyError(f'Сбой "{error}" при запросе к эндпоинту.')
    if homework_status != HTTPStatus.OK:
        raise KeyError(f'Status_code сервера API {homework_status}, а не 200.')
    try:
        response = homeworks.json()
    except Exception as error:
        raise KeyError(f'Сбой "{error}" при переводе в json.')
    return response


def parse_status(homework):
    """Получаем статус последней домашней работы(если она есть)."""
    if 'homework_name' in homework:
        homework_name = homework['homework_name']
    else:
        message = 'API вернул домашнее задание без ключа "homework_name"'
        raise KeyError(message)
    homework_status = homework['status']
    try:
        verdict = HOMEWORK_VERDICTS[homework_status]
    except Exception:
        raise KeyError(
            f'Статуса {homework_status} нет в "HOMEWORK_STATUSES".'
        )
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_response(response):
    """Проверяем наш запрос на предмет различных ошибок."""
    if 'homeworks' not in response:
        message = 'В ответе API нет ключа "homeworks"'
        raise TypeError(message)

    hw_list = response['homeworks']

    if not isinstance(hw_list, list):
        message = ('Тип значения "homeworks" в ответе API'
                   f'"{type(hw_list)}" не является списком'
                   )
        raise TypeError(message)

    return hw_list


def main():
    """Главная функция."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            bot.send_message(TELEGRAM_CHAT_ID, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
