from Figure import *
from tkinter import BOTH


class Ellipse(Figure):

    shapeName = 'ellipse'

    def draw(self):
        """
        Draws the Ellipse on the canvas
        :return:
        """

        self.shape = self.canvas.create_oval(
            self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3],
            outline="#000000", tags=(self.name, self.tag)
        )
        self.canvas.pack(expand=1, fill=BOTH)
