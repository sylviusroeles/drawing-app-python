from FigureVisitor import *


class Move(FigureVisitor):

    coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def visit(self, figure):
        figure.move(self)
