import subprocess
import re

processes = []

while True:
    clients_count = 2
    action = input('Select action: q - exit, s [number] - start server and (number) clients, x - close all terminals: ')

    if re.fullmatch(r's\s\d', action):
        try:
            clients_count = int(action.split(' ')[1])
        except:
            pass
        action = 's'

    if action == 'q':
        break

    elif action == 's':
        processes.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(clients_count):
            processes.append(subprocess.Popen(f'python client.py -n user{i + 1}',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        # for i in range(1):
        #     processes.append(subprocess.Popen(f'python client.py -m listen -n Listener_{i + 1}',
        #                                       creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while processes:
            proc = processes.pop()
            proc.kill()
