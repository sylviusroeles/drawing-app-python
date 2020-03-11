from Commands_Struct import *
from Group import *
from Rectangle import *
from Ellipse import *


class IO:
    COMMAND_INDEX = 0

    grammar = None

    command_chain = []

    file = None

    def __init__(self, filename, canvas):
        """
        :param filename:
        """
        self.grammar = {
            'rectangle': [COMMAND_CREATE, 'rectangle'],
            'ellipse': [COMMAND_CREATE, 'ellipse'],
            'group': [COMMAND_GROUP],
        }
        self.canvas = canvas

        try:
            with open(filename, 'r') as file:
                self.file = file.readlines()
        except:
            pass

    def parse_file(self):
        """
        Parse the file into a command structure
        :return:
        """
        if not self.file:
            return []

        groups_for_indentation = {}

        for line in self.file:
            current_indentation = len(line) - len(line.lstrip())
            commands = line.lstrip().strip('\n').split(' ')
            if commands[self.COMMAND_INDEX] in self.grammar:
                if commands[self.COMMAND_INDEX] == COMMAND_GROUP:
                    group = Group(self.canvas)
                    self.command_chain.append(group)
                    groups_for_indentation[current_indentation + 4] = group
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
                        self.command_chain.append(Rectangle(self.parse_coordinates(commands[1:]), self.canvas))
        return self.command_chain

    @staticmethod
    def parse_coordinates(coordinates):
        """
        Parses coordinates to Tkinter x, y, x1, y1 instead of x, y, width, height
        :param coordinates:
        :return:
        """
        return [
            coordinates[0],
            coordinates[1],
            str(int(coordinates[0]) + int(coordinates[2])),
            str(int(coordinates[1]) + int(coordinates[3])),
        ]
