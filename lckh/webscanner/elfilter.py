import os

from lxml import html


def check_elfilter(et):
    for dbn in os.listdir(os.path.join(os.environ.get('BASEDIR', '../..'), 'blacklist/elfilter')):
        with open(os.path.join(os.environ.get('BASEDIR', '../..'), 'blacklist/elfilter', dbn), 'r') as ifile:
            for chunk in ifile:
                if et.xpath(chunk):
                    yield 1, f"Недопустимое содержимое. Фильтр {os.path.splitext(dbn)[0]}"
