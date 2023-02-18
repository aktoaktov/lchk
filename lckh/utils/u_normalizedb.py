import socket
from enum import Enum
from urllib.parse import urlparse
import datetime
import csv

REGIONS = [

]


class Types(Enum):
    MLW = 1 << 1
    SPY = 1 << 2
    ADV = 1 << 3
    LOCK = 1 << 4
    ELF = 1 << 5
    STEAL = 1 << 6
    RAT = 1 << 7

    @classmethod
    def parse(cls, string: str) -> int:
        r = 0
        for tag in string.split(','):
            match tag:
                case 'elf' | 'ELF':
                    if not r & cls.ELF.value:
                        r += cls.ELF.value
                case 'mlw' | 'MLW' | 'mips' | 'mirai' | 'malware':
                    if not r & cls.MLW.value:
                        r += cls.MLW.value
                case 'spy':
                    if not r & cls.SPY.value:
                        r += cls.SPY.value
                case 'adv':
                    if not r & cls.ADV.value:
                        r += cls.ADV.value
        return r


with open("urlhotlist.csv", "r", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # FOLDER = "urlhaus"
    # f = {r: open(f"{FOLDER}/{r}.dat", "wb") for r in REGIONS}
    wio = open(f'../../blacklist/uries/urlhaus.dat', 'wb')

    for row in reader:
        url = urlparse(row.get('url'))

        if da := row.get("date-added"):
            wio.write(int(datetime.datetime.fromisoformat("2023-02-17 15:23:13").timestamp()).to_bytes(4, 'big'))
        else:
            wio.write(b'\x00\x00\x00\x00')

        if tags := row.get("tags"):
            wio.write(Types.parse(tags).to_bytes(1, 'big'))
        else:
            wio.write(b'\x00')

        wio.write((url.hostname or socket.gethostbyname(url.netloc)).encode('ascii', errors='ignore'))
        wio.write(b'\x00')
        wio.write(url.path.encode('ascii', errors='ignore'))
        wio.write(b'\x0a')
