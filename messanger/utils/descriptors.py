class CheckPort:
    def __get__(self, instance, owner):
        return instance.__dict__[self.my_attr]

    def __set__(self, instance, value):
        if not 1024 <= value <= 65535:
            raise ValueError('Invalid port value. Values from 1024 to 65535 are accepted.')

        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, my_attr):
        self.my_attr = my_attr
