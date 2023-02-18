import ipaddress

with open('Malicious.txt', 'r') as ifile, open('../../blacklist/ips/Malicious.dat', 'wb') as ofile:
    for s in ifile:
        try:
            ofile.write(ipaddress.ip_address(s.strip()).packed + b'\x0a')
        except:
            pass
