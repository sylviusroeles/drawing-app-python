from FigureVisitor import *


class Resize(FigureVisitor):
    """
    Visitor pattern shape Resize function
    """

    coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def visit(self, figure):
        figure.resize(self)