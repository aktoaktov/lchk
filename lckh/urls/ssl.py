import ssl
import socket
import time
from urllib.parse import urlparse

import OpenSSL
from pprint import pprint
from datetime import datetime


def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


def check_cert(url):
    if isinstance(url, str):
        url = urlparse(url)

    try:
        certificate = get_certificate(url.hostname)
    except:
        yield 1, "SSL сертификат отсутствует"
    else:
        cdata = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
        ctime = time.mktime(time.gmtime())

        if (_ := cdata.get_version()) < 2:
            yield 1, f"Недопустимая версия SSL сертификата {_}"

        if ctime <= datetime.strptime(cdata.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ').timestamp():
            yield 1, f"SSL сертификат путешествует в прошлое!"
        elif datetime.strptime(cdata.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').timestamp() >= ctime:
            yield 1, f"SSL сертификат просрочен"

        # TODO: Доделать проверку AKI и компании

        # result = {
        #     'subject': dict(x509.get_subject().get_components()),
        #     'issuer': dict(x509.get_issuer().get_components()),
        #     'serialNumber': x509.get_serial_number(),
        #     'notBefore': datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'),
        #     'notAfter': datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'),
        # }
        #
        # extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
        # extension_data = {e.get_short_name(): str(e) for e in extensions}
        # result.update(extension_data)
