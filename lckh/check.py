from urllib.parse import urlparse
import requests


def check(uri):
    uri = urlparse(uri.strip())

    if uri.scheme in {"file"}:
        yield 1, "Локальный файл"

    else:
        session = requests.Session()


