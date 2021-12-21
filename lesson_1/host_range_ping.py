"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса. По результатам проверки должно выводиться соответствующее
сообщение.
"""

from host_ping import host_ping, get_ip_address


def host_range_ping(first_address, last_address, interactive=True):
    addresses_list = []
    ip_1 = get_ip_address(first_address)
    ip_2 = get_ip_address(last_address)

    if ip_1 and ip_2 and str(ip_1).split('.')[0:3] == str(ip_2).split('.')[0:3] and ip_1 < ip_2:
        while ip_1 <= ip_2:
            addresses_list.append(str(ip_1))
            ip_1 += 1
    else:
        if interactive:
            print('Incorrect range!')
        return None

    return host_ping(addresses_list, interactive)


if __name__ == '__main__':
    host_range_ping('192.168.0.1', '192.168.0.10')
    host_range_ping('192.168.1.1', '192.168.0.10')
