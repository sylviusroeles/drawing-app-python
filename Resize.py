from FigureVisitor import *


class Resize(FigureVisitor):

    coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def visit(self, figure):
        figure.resize(self)