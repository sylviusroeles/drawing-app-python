from Figure import *


class Group(Figure):

    def __init__(self, canvas):
        """
        :param canvas:
        """
        super().__init__(canvas)
        self.shapes = []

    def add(self, shape):
        """
        :param shape:
        :return:
        """
        self.shapes.append(shape)

    def remove(self, shape):
        """
        :param shape:
        :return:
        """
        self.shapes.remove(shape)

    def get_all(self):
        """
        :return:
        """
        return self.shapes
