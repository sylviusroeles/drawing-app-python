from Ellipse import *
from Rectangle import *


class Commands:
    COMMAND_CREATE = 'create'
    COMMAND_SELECT = 'select'
    COMMAND_MOVE = 'move'
    COMMAND_RESIZE = 'resize'

    canvas = None
    current_command = None

    def __init__(self, canvas):
        """
        :param canvas:
        """
        self.canvas = canvas

    def get_current_command(self):
        """
        :return:
        """
        return self.current_command

    def set_current_command(self, command):
        """
        :param command:
        :return:
        """
        self.current_command = command

    def create(self, shape, coordinates):
        """
        :param shape:
        :param coordinates:
        :return:
        """
        if shape is Rectangle.name:
            rectangle = Rectangle(coordinates, self.canvas)
            rectangle.draw()
            return rectangle
        elif shape is Ellipse.name:
            ellipse = Ellipse(coordinates, self.canvas)
            ellipse.draw()
            return ellipse

    def select(self, coordinates):
        """
        :param coordinates:
        :return:
        """
        shape = self.canvas.find_closest(coordinates[0], coordinates[1])
        return self.canvas.gettags(*shape)

    def move(self, shape, coordinates):
        """
        :param shape:
        :param coordinates:
        :return:
        """
        current_coordinates = self.canvas.coords(shape)
        self.canvas.move(shape, coordinates[0] - current_coordinates[0], coordinates[1] - current_coordinates[1])

    def resize(self, shape, coordinates):
        """
        this was literally done by trail and error, thanks to the poor documentation of tkinter
        :param shape:
        :param coordinates:
        :return:
        """
        (x0, y0, x1, y1) = self.canvas.coords(shape)
        width = x0 / coordinates[0]
        height = y0 / coordinates[1]
        x1 = x0 / width
        y1 = y0 / height
        self.canvas.coords(shape, x0, y0, x1, y1)
