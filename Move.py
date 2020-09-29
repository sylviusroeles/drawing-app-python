from FigureVisitor import *


class Move(FigureVisitor):
    """
    Visitor pattern shape Move function
    """
    coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def visit(self, figure):
        figure.move(self)
