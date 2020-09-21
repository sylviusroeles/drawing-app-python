import types


class Strategy:

    execute = None

    def __init__(self, name, function):
        """
        Sets the function to execute for the shape
        :param name:
        :param function:
        """
        self.name = name
        if function:
            self.execute = types.MethodType(function, name)

    def to_string(self):
        print(self.name)
