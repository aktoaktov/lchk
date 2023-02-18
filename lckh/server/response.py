import datetime
import time

import requests
from requests import Session

MAX_TIMEOUT = 12.0
MAX_SDELAY = 60.0
MAX_DATEDIFF = 60.0

MAX_HISTORY_LEN = 4


def check_response(session: Session, uri):
    try:
        with session.head(uri, timeout=MAX_TIMEOUT, allow_redirects=True) as response:

            # Если сервер не так ответил
            if response.status_code in {500, 502, 503, 504, 505, 506, 444, 492, 399, 593}:
                yield 0.8, f"Код состояния {response.status_code} {response.reason or ''}".strip()

            # Проверка, что Date сервера нормальный
            if not response.headers.get('Date'):
                yield 1, f"Отсутствует основной заголовок Date"
            else:
                date = datetime.datetime.strptime(response.headers.get('Date'), "%a, %d %b %Y %H:%M:%S %Z").timestamp()
                if (diff := abs(date - time.mktime(time.gmtime()))) > MAX_DATEDIFF:
                    yield 1, f"Время сервера сильно отличается от времени клиента (на {diff // 60} минут)"

            # Заголовок Server и его специфика (вплоть до версий)
            if not response.headers.get('Server'):
                yield 1, f"Отсутствует основной заголовок Server"
            else:
                # TODO: Проверять сервера и актуальные версии
                pass

            # Перенаправления
            if response.history:
                if (_ := len(response.history)) >= MAX_HISTORY_LEN:
                    yield 1, f"Много перенаправлений ({_})"

    except requests.Timeout:
        yield 1, f"Сервер отвечал больше {MAX_TIMEOUT} секунд"
    except TimeoutError:
        yield 1, "Сервер не отвечает"
