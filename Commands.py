from tkinter import ALL
from Ellipse import *
from Rectangle import *
from IO import *
from Commands_Struct import *


class Commands:
    # stack for redo/undo
    command_stack = []
    command_stack_pointer = 0
    command_stack_name_index = 0
    command_stack_args_index = 1

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
        args = (coordinates, self.canvas)

        if shape is Rectangle.name:
            rectangle = Rectangle(*args)
            rectangle.draw()
            self.command_stack_push(COMMAND_REDRAW, rectangle)
            return rectangle
        elif shape is Ellipse.name:
            ellipse = Ellipse(*args)
            ellipse.draw()
            self.command_stack_push(COMMAND_REDRAW, ellipse)
            return ellipse

    @staticmethod
    def redraw(shape):
        """
        Function to redraw a shape after a undo or redo action
        :param shape:
        :return:
        """
        shape.draw()

    def select(self, coordinates):
        """
        :param coordinates:
        :return:
        """
        shape = self.canvas.find_closest(coordinates[0], coordinates[1])
        return self.canvas.gettags(*shape)

    def move(self, shape, coordinates, push_to_command_stack=True):
        """
        :param push_to_command_stack:
        :param shape:
        :param coordinates:
        :return:
        """
        if not shape:
            return
        if push_to_command_stack:
            self.command_stack_push(COMMAND_MOVE, shape, coordinates, False)
        current_coordinates = self.canvas.coords(shape)
        self.canvas.move(shape, coordinates[0] - current_coordinates[0], coordinates[1] - current_coordinates[1])

    def resize(self, shape, coordinates, push_to_command_stack=True):
        """
        this was literally done by trail and error, thanks to the poor documentation of tkinter
        :param push_to_command_stack:
        :param shape:
        :param coordinates:
        :return:
        """
        if not shape:
            return
        if push_to_command_stack:
            self.command_stack_push(COMMAND_RESIZE, shape, coordinates, False)
        (x0, y0, x1, y1) = self.canvas.coords(shape)
        width = x0 / coordinates[0]
        height = y0 / coordinates[1]
        x1 = x0 / width
        y1 = y0 / height
        self.canvas.coords(shape, x0, y0, x1, y1)

    def command_stack_push(self, command_name, *args):
        """
        Pushes command to the command stack
        :param command_name:
        :return:
        """
        self.command_stack.insert(0, [command_name, args])

    def undo(self):
        """
        Handles the undo command
        :return:
        """
        self.canvas.delete(ALL)
        if self.command_stack_pointer + 1 <= len(self.command_stack):
            self.command_stack_pointer += 1  # prevent out of bounds stack pointer
        self.redraw_canvas()

    def redo(self):
        """
        Handles the redo command
        :return:
        """
        self.canvas.delete(ALL)
        if self.command_stack_pointer - 1 >= 0:
            self.command_stack_pointer -= 1  # prevent negative stack pointer
        self.redraw_canvas()

    def import_(self, filename):
        """
        Handles the import command
        :return:
        """
        commands = IO(filename).parse_file()
        for command in commands:
            print(command)
            command_name = command[0]
            command_args = command[1:]
            getattr(self, command_name)(*command_args)

    def redraw_canvas(self):
        """
        Redraws the canvas based on the stack pointer
        :return:
        """
        for command_index in range(len(self.command_stack)-1, self.command_stack_pointer-1, -1):
            command = self.command_stack[command_index]
            command_name = command[self.command_stack_name_index]
            command_args = command[self.command_stack_args_index]
            getattr(self, command_name)(*command_args)
