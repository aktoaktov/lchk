from lxml import html


def parse(responce):
    return html.fromstring(responce.content)
