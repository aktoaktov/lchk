import time
from urllib.parse import urlparse

from whois import whois


def check_whois(url):
    if isinstance(url, str):
        url = urlparse(url)

    wd = whois(url.hostname)
    statuses = set(wd.get('status').split(', '))

    if wd.get('expiration_date').timestamp() <= time.mktime(time.gmtime()):
        yield "Просроченная регистрация"

    if 'REGISTERED' not in statuses or 'VERIFIED' not in statuses:
        yield "Неверный статус у регистратора"

    # TODO: По-хорошему нужна проверка registrar и org
