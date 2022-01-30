"""
1. Реализовать метакласс ClientVerifier, выполняющий базовую проверку класса «Клиент» (для некоторых проверок уместно
использовать модуль dis):
    отсутствие вызовов accept и listen для сокетов;
    использование сокетов для работы по TCP;
    отсутствие создания сокетов на уровне классов, то есть отсутствие конструкций такого вида:
        class Client: s = socket() ...

2. Реализовать метакласс ServerVerifier, выполняющий базовую проверку класса «Сервер»:

    отсутствие вызовов connect для сокетов;
    использование сокетов для работы по TCP.

"""
import types
import dis


class ServerVerifier(type):
    def __init__(cls, name, bases, dict):
        attrs = set()
        for val in dict.values():
            if isinstance(val, types.FunctionType):
                dis_res = dis.get_instructions(val)
                for inst in dis_res:
                    if inst.opname == 'LOAD_GLOBAL' and inst.argval == 'connect':
                        raise SyntaxError('You cannot use call connections for sockets ')
                    elif inst.opname == 'LOAD_ATTR':
                        attrs.add(inst.argval)
        print(attrs)
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise SyntaxError('Only TCP protocol supported for socket')

        super(ServerVerifier, cls).__init__(name, bases, dict)


class ClientVerifier(type):
    def __init__(cls, name, bases, dict):
        print(f'__init__({name}, {bases}, {dict})')
        attrs = set()
        methods = []
        for val in dict.values():
            if isinstance(val, types.FunctionType):
                print('__init__ (val):', val)
                dis_res = dis.get_instructions(val)
                for inst in dis_res:
                    if inst.opname == 'LOAD_GLOBAL':
                        methods.append(inst.argval)
                    elif inst.opname == 'LOAD_ATTR':
                        attrs.add(inst.argval)
        print(' *********** methods:', methods)
        print(' *********** attrs:', attrs)

        for method in methods:
            if method in ('accept', 'listen', 'socket'):
                raise SyntaxError('You cannot use call accept and listen methods for Client.')

        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise SyntaxError('Only TCP protocol supported for socket')

        super(ClientVerifier, cls).__init__(name, bases, dict)
