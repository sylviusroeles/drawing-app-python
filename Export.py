from FigureVisitor import *


class Export(FigureVisitor):
    """
    Visitor pattern shape Export function
    """

    def __init__(self, coordinates, name):
        self.coordinates = coordinates
        self.name = name

    def visit(self, figure):
        return figure.export(self)
