from Commands_Struct import *
from Export import *
from Group import *
from Rectangle import *
from Ellipse import *
from Commands import *


class IO:
    COMMAND_INDEX = 0

    rectangle = Rectangle()
    ellipse = Ellipse()

    grammar = None

    def __init__(self, canvas):
        self.grammar = {
            'rectangle': [COMMAND_CREATE, 'rectangle'],
            'ellipse': [COMMAND_CREATE, 'ellipse'],
            'group': [COMMAND_GROUP],
            'ornament': [COMMAND_DESCRIPTION]
        }
        self.canvas = canvas
        self.command_chain = []

    def parse_file(self, filename):
        """
        Parse the file into a command structure
        :return:
        """
        try:
            with open(filename, 'r') as file:
                file = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError('File not found')

        if not file:
            return []

        groups_for_indentation = {}
        descriptions_for_next_shape = []

        for line in file:
            current_indentation = len(line) - len(line.lstrip())
            commands = line.lstrip().strip('\n').split(' ')
            if commands[self.COMMAND_INDEX] in self.grammar:

                if commands[self.COMMAND_INDEX] == COMMAND_GROUP:
                    group = Group(self.canvas)
                    self.command_chain.append(group)
                    groups_for_indentation[current_indentation + 4] = group

                    if current_indentation in groups_for_indentation:
                        groups_for_indentation[current_indentation].add(group)
                        descriptions_for_next_shape = []

                elif commands[self.COMMAND_INDEX] == self.rectangle.shapeName:
                    rectangle = Figure(self.parse_coordinates(commands[1:]), self.canvas, self.rectangle.shapeName,
                                       self.rectangle)
                    rectangle.strategy = RectangleStrategy()

                    if descriptions_for_next_shape:
                        for description in descriptions_for_next_shape:
                            print(description, vars(rectangle))
                            self.add_description_to_shape(rectangle, *description)

                    if current_indentation in groups_for_indentation:
                        groups_for_indentation[current_indentation].add(rectangle)
                    else:
                        self.command_chain.append(rectangle)
                        descriptions_for_next_shape = []

                elif commands[self.COMMAND_INDEX] == self.ellipse.shapeName:
                    ellipse = Figure(self.parse_coordinates(commands[1:]), self.canvas, self.ellipse.shapeName,
                                     self.ellipse)
                    ellipse.strategy = EllipseStrategy()

                    if descriptions_for_next_shape:
                        for description in descriptions_for_next_shape:
                            print(description, vars(ellipse))
                            self.add_description_to_shape(ellipse, *description)

                    if current_indentation in groups_for_indentation:
                        groups_for_indentation[current_indentation].add(ellipse)
                    else:
                        self.command_chain.append(ellipse)
                        descriptions_for_next_shape = []

                elif commands[self.COMMAND_INDEX] == COMMAND_DESCRIPTION:
                    (position, text) = commands[1:]
                    descriptions_for_next_shape += [[position.capitalize(), text.replace("\"","")]]

        return self.command_chain

    def add_description_to_shape(self, shape, position, description):
        """
        :param shape:
        :param position:
        :param description:
        :return:
        """
        if position == "Left":
            shape.set_description(Left(Description(description, self.canvas)))
        elif position == "Right":
            shape.set_description(Right(Description(description, self.canvas)))
        elif position == "Top":
            shape.set_description(Top(Description(description, self.canvas)))
        elif position == "Bottom":
            shape.set_description(Bottom(Description(description, self.canvas)))
        return shape

    def shapes_to_text(self, shapes, indentation=0, lines=None):
        """
        :param lines:
        :param indentation:
        :param shapes:
        :return:
        """
        if lines is None:
            lines = []
        lines = lines

        indentation = indentation
        for shape in shapes:
            if isinstance(shape, Group):
                lines.append("%sgroup %s" % (self.add_indentation(indentation), len(shape.get_all())))
                indentation += 4
                self.shapes_to_text(
                    [_shapes for _shapes in shape.get_all() if type(_shapes) != Group],
                    indentation,
                    lines)  # make sure to skip all nested groups to prevent more shapes being exported than displayed
            elif type(shape) == Figure:
                lines.append(self.shape_to_command(shape, indentation))
        return '\n'.join(lines)

    def shape_to_command(self, figure, indentation):
        """
        :param figure:
        :param indentation:
        :return:
        """
        shape_command = figure.accept(
            Export(figure.coordinates, figure.shape.shapeName if type(figure) == Figure else figure.shapeName))
        return "%s%s" % (
            self.add_indentation(indentation),
            shape_command
        )

    @staticmethod
    def add_indentation(indentation):
        """
        Adds indentation spaces
        :param indentation:
        :return:
        """
        return ''.join([' ' for i in range(0, indentation)])

    @staticmethod
    def parse_coordinates(coordinates):
        """
        Parses coordinates to Tkinter x, y, x1, y1 instead of x, y, width, height
        :param coordinates:
        :return:
        """
        return [
            int(coordinates[0]),
            int(coordinates[1]),
            int(str(int(coordinates[0]) + int(coordinates[2]))),
            int(str(int(coordinates[1]) + int(coordinates[3]))),
        ]
