from tkinter import ALL

from Decorators.Left import Left
from Decorators.Right import Right
from Decorators.Description import Description
from Decorators.Top import Top
from Decorators.Bottom import Bottom
from Move import *
from Resize import *
from IO import *
from Commands_Struct import *
from Ellipse import *
from Rectangle import *


class Commands:

    rectangle = Rectangle()
    ellipse = Ellipse()

    def __init__(self, canvas, current_shape_list):
        """
        :param canvas:
        """
        self.canvas = canvas
        self.current_shape_list = current_shape_list
        self.TAG_ID = 1

        # stack for redo/undo
        self.command_stack = []
        self.command_stack_pointer = 0
        self.command_stack_name_index = 0
        self.command_stack_args_index = 1

        self.current_command = None

    def set_current_shape_list(self, shape_list):
        self.current_shape_list = shape_list
        return self

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
        if shape is Rectangle.shapeName:
            rectangle = Figure(*args, 'rectangle', self.rectangle)
            rectangle.strategy = RectangleStrategy()
            rectangle.draw()
            self.command_stack_push(COMMAND_REDRAW, rectangle)
            return rectangle
        elif shape is Ellipse.shapeName:
            ellipse = Figure(*args, 'ellipse', self.ellipse)
            ellipse.strategy = EllipseStrategy()
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

    def select(self, coordinates, group_list):
        """
        :param group_list:
        :param coordinates:
        :return:
        """
        closest_shape = self.canvas.find_closest(coordinates[0], coordinates[1])
        if closest_shape:
            selected_tag = self.canvas.gettags(*closest_shape)[self.TAG_ID]
            shape_object = None

            for shape in self.current_shape_list:
                if shape.tag == selected_tag:
                    shape_object = shape

            if not shape_object:
                return None

            for group in group_list:
                return self.get_shape_in_nested_group(group, shape_object)

            return [shape_object]
        return None

    def get_shape_in_nested_group(self, group, shape_object):
        """
        Gets a shape from nested groups
        :param group:
        :param shape_object:
        :return:
        """
        for shape in group.get_all():
            if isinstance(shape, Group):
                self.get_shape_in_nested_group(shape, shape_object)
            elif shape.tag == shape_object.tag:
                return group.get_all()
        return [shape_object]


    def move(self, shapes_list, coordinates, push_to_command_stack=True):
        """
        :param push_to_command_stack:
        :param shapes_list:
        :param coordinates:
        :return:
        """
        if not shapes_list:
            return False

        if push_to_command_stack:
            self.command_stack_push(COMMAND_MOVE, shapes_list, coordinates, False)

        for shape in shapes_list:
            shape.accept(Move(coordinates))

    def resize(self, shape_list, coordinates, push_to_command_stack=True):
        """
        this was literally done by trail and error, thanks to the poor documentation of tkinter
        :param push_to_command_stack:
        :param shape_list:
        :param coordinates:
        :return:
        """
        if not shape_list:
            return False

        if push_to_command_stack:
            self.command_stack_push(COMMAND_RESIZE, shape_list, coordinates, False)

        for shape in shape_list:
            (x0, y0, x1, y1) = self.canvas.coords(shape.tag)
            width = x0 / coordinates[0]
            height = y0 / coordinates[1]
            x1 = x0 / width
            y1 = y0 / height
            shape.accept(Resize([x0, y0, x1, y1]))

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
        shapes = IO(self.canvas).parse_file(filename)
        self.current_shape_list += shapes
        for shape in shapes:
            if isinstance(shape, Group):
                for _shape in shape.get_all():
                    if isinstance(_shape, Group) or _shape.tag is None:
                        continue
                    _shape.draw()
                    if _shape.descriptions is not None:
                        _shape.render_description()
            else:
                shape.draw()
                if shape.descriptions is not None:
                    shape.render_description()
        return shapes

    def export_(self):
        return IO(self.canvas).shapes_to_text(self.current_shape_list)

    def group(self, shapes, push_to_command_stack=True):
        """
        Handles the group command
        :param push_to_command_stack:
        :param shapes:
        :return:
        """
        if not shapes:
            return False

        group = Group(self.canvas)
        for shape in shapes:
            group.add(shape)
        if push_to_command_stack:
            self.command_stack_push(COMMAND_GROUP, shapes, False)
        return group

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

    def description(self, selected_shapes, description, position, push_to_command_stack=True):
        """
        :param push_to_command_stack:
        :param selected_shapes:
        :param description:
        :param position:
        :return:
        """
        if push_to_command_stack:
            self.command_stack_push(COMMAND_DESCRIPTION, selected_shapes, description, position, False)

        for selected_shape in selected_shapes:
            if not push_to_command_stack: #undo or redo triggered. Reset descriptions in Figure object to prevent double drawing
                selected_shape.descriptions = None

            if position == "Left":
                selected_shape.set_description(Left(Description(description, self.canvas)))
            elif position == "Right":
                selected_shape.set_description(Right(Description(description, self.canvas)))
            elif position == "Top":
                selected_shape.set_description(Top(Description(description, self.canvas)))
            elif position == "Bottom":
                selected_shape.set_description(Bottom(Description(description, self.canvas)))
            selected_shape.render_description()