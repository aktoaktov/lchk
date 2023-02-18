import datetime
import ipaddress
import os
import socket

from urllib.parse import urlparse


def check_bldb(url):
    if isinstance(url, str):
        url = urlparse(url)

    domain, aliases, ips = socket.gethostbyname_ex(url.hostname)

    for dbn in os.listdir(os.path.join(os.environ.get('BASEDIR', '../blacklist'), 'blacklist/uries')):
        with open(os.path.join(os.environ.get('BASEDIR', '../blacklist'), 'blacklist/uries', dbn), 'rb') as ifile:
            for chunk in ifile:
                try:
                    date, tags, addr, path = chunk[:4], chunk[4], *chunk[5:].split(b'\x00', 1)
                    if addr.decode('ascii') in set(aliases) | set(ips) | {domain}:
                        # TODO: отформатировать, tags - <Types(int)> теги типа ресурса
                        yield 2, f"ЧС База {os.path.splitext(dbn)[0]}: {datetime.datetime.fromtimestamp(int.from_bytes(date, 'big')).strftime('%d.%m.%Y, %H:%M:%S')}"
                except:
                    pass

    for dbn in os.listdir(os.path.join(os.environ.get('BASEDIR', '../blacklist'), 'blacklist/ips')):
        with open(os.path.join(os.environ.get('BASEDIR', '../blacklist'), 'blacklist/ips', dbn), 'rb') as ifile:
            for chunk in ifile:
                try:
                    if str(ipaddress.ip_address(chunk.strip())) in set(aliases) | set(ips):
                        # TODO: отформатировать
                        yield 2, f"ЧС IP База {os.path.splitext(dbn)[0]}"
                except:
                    pass
