from Commands_Struct import *
from Export import *
from Group import *
from Rectangle import *
from Ellipse import *


class IO:
    COMMAND_INDEX = 0

    grammar = None

    def __init__(self, canvas):
        self.grammar = {
            'rectangle': [COMMAND_CREATE, 'rectangle'],
            'ellipse': [COMMAND_CREATE, 'ellipse'],
            'group': [COMMAND_GROUP],
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
                elif commands[self.COMMAND_INDEX] == 'rectangle':
                    if current_indentation in groups_for_indentation:
                        groups_for_indentation[current_indentation].add(
                            Rectangle(self.parse_coordinates(commands[1:]), self.canvas))
                    else:
                        self.command_chain.append(Rectangle(self.parse_coordinates(commands[1:]), self.canvas))
                elif commands[self.COMMAND_INDEX] == 'ellipse':
                    if current_indentation in groups_for_indentation:
                        groups_for_indentation[current_indentation].add(
                            Ellipse(self.parse_coordinates(commands[1:]), self.canvas))
                    else:
                        self.command_chain.append(Ellipse(self.parse_coordinates(commands[1:]), self.canvas))
        return self.command_chain

    def shapes_to_text(self, shapes):
        """
        :param shapes:
        :return:
        """
        lines = []
        indentation = 0
        for shape in shapes:
            if isinstance(shape, Group):
                lines.append("%sgroup %s" % (self.add_indentation(indentation), len(shape.get_all())))
                indentation += 4
                for _shape in shape.get_all():
                    if isinstance(_shape, Rectangle) or isinstance(_shape, Ellipse):
                        lines.append(self.shape_to_command(_shape, indentation))
            elif isinstance(shape, Rectangle) or isinstance(shape, Ellipse):
                lines.append(self.shape_to_command(shape, indentation))
        return '\n'.join(lines)

    def shape_to_command(self, shape, indentation):
        """
        :param shape:
        :param indentation:
        :return:
        """
        shape_command = shape.accept(Export(shape.coordinates, shape.name))
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
