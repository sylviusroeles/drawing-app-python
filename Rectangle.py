from Figure import *
from tkinter import BOTH


class Rectangle(Figure):

    name = 'rectangle'
    tag = None

    def __init__(self, coordinates, canvas):
        """
        :param coordinates:
        :param canvas:
        """
        super().__init__(canvas)
        self.coordinates = coordinates
        self.shape = 0
        self.tag = self.name + str(id(self))

    def draw(self):
        """
        Draws the Rectangle on the canvas
        :return:
        """
        self.shape = self.canvas.create_rectangle(
            self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3],
            outline="#000000", tags=(self.name, self.tag)
        )
        self.canvas.pack(expand=1, fill=BOTH)
