"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""
import re
import subprocess
import socket
from ipaddress import ip_address
import platform

from chardet import detect

CODE = '-n' if platform.system() == 'Windows' else '-c'


def ping(ip):
    subproc_ping = subprocess.Popen(['ping', CODE, '1', ip], stdout=subprocess.PIPE)
    for reply in subproc_ping.stdout:
        code = detect(reply)['encoding']
        reply = reply.decode(code).encode('utf-8').decode('utf-8')
        if re.search("100%", reply):
            return False
        elif re.search("0%", reply):
            return True
        else:
            continue


def get_ip_address(host):
    try:
        ip_addr = ip_address(host)
    except ValueError:
        try:
            ip_addr = ip_address(socket.gethostbyname(host))
        except (ValueError, socket.gaierror):
            return None
    return ip_addr


def host_ping(hosts, interactive=True):
    reachable_hosts = []
    unreachable_hosts = []
    unresolved_hostnames = []
    addresses = {}

    for host in hosts:
        if addresses.get(host):
            continue
        ip_addr = get_ip_address(host)
        if ip_addr:
            addresses[host] = ip_addr
        else:
            unresolved_hostnames.append(host)

    for host in addresses.keys():
        if ping(str(addresses[host])):
            reachable_hosts.append({'host': host, 'address': addresses[host]})
            if interactive:
                print(f'Host {host} is reachable.')
        else:
            unreachable_hosts.append({'host': host, 'address': addresses[host]})
            if interactive:
                print(f'Host {host} is unreachable.')

    if unresolved_hostnames and interactive:
        print('List of unresolved host names:', unresolved_hostnames)

    return reachable_hosts, unreachable_hosts, unresolved_hostnames


if __name__ == '__main__':
    test_hosts = ['8.8.8.8', '10.10.10.100', 'yandex.ru', 'localhost', 'asdfdsf', 'mail.ru', 'localhost']
    host_ping(test_hosts)
