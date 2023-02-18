import os
from urllib.parse import urlparse

from adblockparser import AdblockRules


def check_ablock(url):
    if isinstance(url, str):
        url = urlparse(url).geturl()
    else:
        url = url.geturl()

    for dbn in os.listdir(os.path.join(os.environ.get('BASEDIR', '../..'), 'blacklist/ablock')):
        with open(os.path.join(os.environ.get('BASEDIR', '../..'), 'blacklist/ablock', dbn), 'r') as ifile:
            ruller = AdblockRules(ifile.read().splitlines())
            if ruller.should_block(url):
                yield 1, f"Фильтр {os.path.splitext(dbn)[0]}"



check_ablock('https://somedomain.com/tracking')
