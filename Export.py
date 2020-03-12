from FigureVisitor import *


class Export(FigureVisitor):

    def __init__(self, coordinates, name):
        self.coordinates = coordinates
        self.name = name

    def visit(self, figure):
        return figure.export(self)
