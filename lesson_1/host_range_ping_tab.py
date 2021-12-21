"""
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate).
"""

from tabulate import tabulate

from host_range_ping import host_range_ping


def host_range_ping_tab(first_address, last_address):
    print('Scanning in progress...')
    result = host_range_ping(first_address, last_address, interactive=False)

    if result is None:
        print('Incorrect address range!')
        return

    reachable_hosts, unreachable_hosts, _ = result
    reachable_hosts = [item['host'] for item in reachable_hosts]
    unreachable_hosts = [item['host'] for item in unreachable_hosts]

    print(f'Results of scanning address from {first_address} to {last_address}:\n ')
    print(tabulate({'Reachable': reachable_hosts, 'Unreachable': unreachable_hosts}, headers='keys', tablefmt="pipe"))


if __name__ == '__main__':
    print()
    host_range_ping_tab('192.168.1.5', '192.168.1.10')
