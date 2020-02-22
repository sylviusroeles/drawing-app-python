from Commands_Struct import *


class IO:

    COMMAND_INDEX = 0

    grammar = None

    command_chain = []

    file = None

    def __init__(self, filename):
        """
        :param filename:
        """
        self.grammar = {
            'rectangle': [COMMAND_CREATE, 'rectangle'],
            'ellipse': [COMMAND_CREATE, 'ellipse'],
        }

        with open(filename, 'r') as file:
            self.file = file.readlines()

    def parse_file(self):
        """
        Parse the file into a command structure
        :return:
        """
        for line in self.file:
            commands = line.strip('\n').split(' ')
            if commands[self.COMMAND_INDEX] in self.grammar:
                print(commands[self.COMMAND_INDEX])
                if commands[self.COMMAND_INDEX] == 'rectangle' or commands[self.COMMAND_INDEX] == 'ellipse':
                    # parse coordinates if rectangle or ellipse
                    self.command_chain.append(
                        [*self.grammar[commands[self.COMMAND_INDEX]], (self.parse_coordinates(commands[1:]))])
                else:
                    self.command_chain.append([*self.grammar[commands[self.COMMAND_INDEX]], (commands[1:])])
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
