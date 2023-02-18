import os
from urllib.parse import urlparse
from Levenshtein import distance


def check_fishing(url):
    if isinstance(url, str):
        url = urlparse(url)

    if url.hostname:
        if '..' in url.hostname:
            yield 1, "Уязвимость: подмена домена"

        if len(domains := url.hostname.split('.')) >= 4:
            yield 0.9, "Слишком много уровней домена"

        if len(url.hostname) >= 54:
            yield 0.3, "Слишком длинный адрес"

        if url.port not in {433, 80}:
            yield 0.6, "Нестандартный порт"

        with open(os.path.join(os.environ.get('BASEDIR', '../blacklist'), 'blacklist/topsites.dat'), 'r') as ffile:
            for site in ffile:
                if 0 < distance(site.strip(), url.hostname) <= 2:
                    yield 3, "Фишинговый сайт"
