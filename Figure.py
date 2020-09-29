from Strategy import *
from tkinter import CENTER
import time

X1 = 0
Y1 = 1
X2 = 2
Y2 = 3


class Figure:
    name = None
    tag = None
    coordinates = None
    shape = None
    descriptions = None

    def __init__(self, coordinates=None, canvas=None, name=None, shape=None, strategy=None):
        """
        :param canvas:
        """
        self.canvas = canvas
        if name:
            self.tag = name + str(id(self))
        self.shape = shape
        self.coordinates = coordinates
        self.strategy = strategy
        self.descriptions = []
        self.description_figures = []

    def accept(self, visitor):
        return visitor.visit(self)

    def set_active_state(self):
        """
        Gives the shape a red outline indicating it's active state
        :return:
        """
        self.canvas.itemconfigure(self.tag, outline='#ff0000')

    def set_inactive_state(self):
        """
        Sets the shape outline to the black inactive state
        :return:
        """
        self.canvas.itemconfigure(self.tag, outline='#000000')

    def move(self, visitor):
        """
        :param visitor:
        :return:
        """
        coordinates = visitor.coordinates
        self.canvas.move(
            self.tag,
            coordinates[X1] - self.coordinates[X1],
            coordinates[Y1] - self.coordinates[Y1]
        )
        self.coordinates = self.canvas.coords(self.canvas.find_withtag(self.tag))
        self.redraw_descriptions()

    def draw(self):
        """
        Executes the strategy pattern to draw a shape
        :return:
        """
        self.shape.coordinates = self.coordinates
        self.shape.canvas = self.canvas
        self.shape.name = self.name
        self.shape.tag = self.tag
        self.strategy.execute(self.shape)
        self.render_description()

    def resize(self, visitor):
        """
        :param visitor:
        :return:
        """
        coordinates = visitor.coordinates
        self.canvas.coords(self.tag, coordinates[X1], coordinates[Y1], coordinates[X2], coordinates[Y2])
        self.redraw_descriptions()

    @staticmethod
    def parse_coordinates(coordinates):
        """
        :param coordinates:
        :return:
        """
        return [
            str(coordinates[X1]),
            str(coordinates[Y1]),
            str(int(coordinates[X2]) - int(coordinates[X1])),
            str(int(coordinates[Y2]) - int(coordinates[Y1])),
        ]

    def export(self, visitor):
        """
        :param visitor:
        :return:
        """
        name = visitor.name
        coordinates = self.parse_coordinates(visitor.coordinates)
        return "%s %s" % (
            name,
            ' '.join([str(coordinate).split('.')[0] for coordinate in coordinates]) #remove decimals
        )

    def get_description(self):
        """
        Gets the description
        :return:
        """
        return self.descriptions

    def set_description(self, description):
        """
        Sets the description of the figure
        :param description:
        :return:
        """
        if not self.descriptions:
            self.descriptions = []

        self.descriptions += [description]

    def render_description(self):
        """
        :return:
        """
        for description in self.descriptions:

            for position in description.render():
                coordinates = self.canvas.coords(self.canvas.find_withtag(self.tag))

                if not coordinates:
                    continue

                if position == "Bottom":
                    self.draw_description([coordinates[X1] + ((coordinates[X2] - coordinates[X1]) / 2),
                                           coordinates[Y2] + 10], description.render()[position])
                if position == "Top":
                    self.draw_description([coordinates[X1] + ((coordinates[X2] - coordinates[X1]) / 2),
                                           coordinates[Y1] - 10], description.render()[position])
                if position == "Left":
                    self.draw_description([coordinates[X1] - 10,
                                           coordinates[Y1] + ((coordinates[Y2] - coordinates[Y1]) / 2)], description.render()[position], 90)
                if position == "Right":
                    self.draw_description([coordinates[X2] + 10,
                                           coordinates[Y1] + ((coordinates[Y2] - coordinates[Y1]) / 2)], description.render()[position], 270)

    def draw_description(self, coordinates, text, angle=0):
        """
        :param coordinates:
        :param text:
        :param angle:
        :return:
        """
        tag = "%s%s%s" % ("description", text, str(round(time.time() * 1000)))
        self.canvas.create_text(*coordinates, anchor=CENTER, text=text, angle=angle, tag=tag)
        self.description_figures += [tag]
        self.canvas.pack()

    def redraw_descriptions(self):
        """
        :return:
        """
        for description_figure in self.description_figures:
            for shape in self.canvas.find_withtag(description_figure):
                self.canvas.delete(shape)
        self.render_description()
