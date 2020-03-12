import types


class Strategy:
    def __init__(self, name, function):
        self.name = name
        if function:
            self.execute = types.MethodType(function, self)

    def to_string(self):
        pass
        # print(self.name)
