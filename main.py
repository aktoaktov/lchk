import os

from flask import Flask, request, render_template

from lckh.server import *
from lckh.urls import *

os.environ['BASEDIR'] = os.getcwd()

app = Flask(__name__)


@app.route('/')
def index():
    if not (q := request.args.get('q')):
        return render_template('index.html')

    dist = 0  # Количество штрафных очков
    verdict = ""

    main, server, pens, sandbox, ext = [], [], [], [], []

    for res in check_bldb(q):
        dist += res[0]
        if not verdict:
            verdict = "Страница в чс"

        main.append(res)

    return render_template('check.html', verdict=verdict, dist=dist, main=main, server=server, pens=pens,
                           sandbox=sandbox, ext=ext)


# session = requests.Session()
#
# for e in check_response(session, "https://httpbin.org/redirect/15"):
#     print(e)
#
# for e in check_bldb('https://cloudstarsolution.com/'):
#     print(e)
#
# for e in check_whois('https://sc15sarov.ru/'):
#     print(e)

if __name__ == '__main__':
    app.run()
