import unittest
from tkinter import *
from Commands import *
from Rectangle import *
from Ellipse import *


class TestCommands(unittest.TestCase):

    def setUp(self) -> None:
        self.current_shapes_list = []

    def create_rectangle(self, canvas, coordinates=None):
        commands = Commands(canvas, self.current_shapes_list)
        if coordinates:
            return commands.create(Rectangle.name, coordinates)
        else:
            return commands.create(Rectangle.name, [100, 100, 200, 200])

    def create_ellipse(self, canvas, coordinates=None):
        commands = Commands(canvas, self.current_shapes_list)
        if coordinates:
            # Allow overloading
            return commands.create(Ellipse.name, coordinates)
        else:
            return commands.create(Ellipse.name, [200, 200, 300, 300])

    def test_create_rectangle_should_return_object(self):
        rectangle = self.create_rectangle(Canvas())
        self.assertIsNotNone(rectangle)
        self.assertIsNotNone(rectangle.tag)

    def test_create_ellipse_should_return_object(self):
        ellipse = self.create_ellipse(Canvas())
        self.assertIsNotNone(ellipse)
        self.assertIsNotNone(ellipse.tag)

    def test_select_with_no_shapes_on_canvas_should_return_none(self):
        selected_shape = Commands(Canvas(), self.current_shapes_list).select([0, 0], [])
        self.assertIsNone(selected_shape)

    def test_select_with_1_shape_should_return_1_shape(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas)
        self.current_shapes_list = []  # empty the current_shape_list
        self.current_shapes_list.append(ellipse)
        ellipse.draw()
        canvas.pack()
        selected_shape = Commands(canvas, self.current_shapes_list).select([0, 0], [])
        self.assertEqual(len(selected_shape), 1)
        self.assertEqual(selected_shape[0].tag, ellipse.tag)

    def test_select_with_2_shapes_on_canvas_should_return_closest(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [100, 100, 160, 160])
        self.current_shapes_list = []  # empty the current_shape_list
        self.current_shapes_list.extend((ellipse, rectangle))
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        selected_shape = Commands(canvas, self.current_shapes_list).select([25, 25], [])
        self.assertEqual(len(selected_shape), 1)
        self.assertEqual(selected_shape[0].tag, ellipse.tag)

    def test_select_where_shape_is_part_of_group_should_return_group_of_shapes(self):
        canvas = Canvas()
        ellipse1 = self.create_ellipse(canvas, [100, 100, 105, 105])
        ellipse2 = self.create_ellipse(canvas, [110, 110, 120, 120])
        rectangle1 = self.create_rectangle(canvas, [130, 130, 140, 140])
        ellipse1.draw()
        ellipse2.draw()
        rectangle1.draw()
        canvas.pack()
        group = Group(canvas)
        group.add(ellipse1)
        group.add(ellipse2)
        group.add(rectangle1)
        selected_shape = Commands(canvas, [ellipse1, ellipse2, rectangle1]).select([150, 150], [group])
        self.assertEqual(len(selected_shape), 3)
        self.assertListEqual(selected_shape, [ellipse1, ellipse2, rectangle1])
        list_of_tags = [s.tag for s in selected_shape]
        self.assertTrue(ellipse1.tag in list_of_tags, "Tag %s not found in %s" % (ellipse1.tag, selected_shape))
        self.assertTrue(ellipse2.tag in list_of_tags)
        self.assertTrue(rectangle1.tag in list_of_tags)

    def test_function_move_should_fail_if_shape_parameter_is_empty(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [100, 100, 105, 105])
        ellipse.draw()
        canvas = Canvas()
        canvas.pack()
        output = Commands(canvas, [ellipse]).move([], [120, 120])
        self.assertFalse(output)

    def test_function_move_should_fail_if_shape_coordinates_are_not_found(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [100, 100, 105, 105])
        ellipse.draw()
        # self.canvas.pack()
        output = Commands(canvas, [ellipse]).move([ellipse], [120, 120])
        self.assertFalse(output)

    def test_function_move_should_move_1_object_if_1_selected(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).move([rectangle], [400, 400])
        self.assertIsNone(output)
        rectangle_coordinates = canvas.coords(rectangle.tag)
        self.assertListEqual(rectangle_coordinates, [300 + 100, 300 + 100, 400 + 100, 400 + 100])

    def test_function_move_should_move_2_objects_if_2_selected(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).move([ellipse, rectangle], [400, 400])
        self.assertIsNone(output)
        rectangle_coordinates = canvas.coords(rectangle.tag)
        ellipse_coordinates = canvas.coords(ellipse.tag)
        self.assertListEqual(rectangle_coordinates, [400, 400, 500, 500])
        self.assertListEqual(ellipse_coordinates, [400, 400, 450, 450])

    def test_function_resize_should_fail_if_no_shape_is_set(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).resize([], [400, 400])
        self.assertFalse(output)

    def test_function_resize_should_resize_1_shape_if_1_selected(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).resize([ellipse], [400, 400])
        self.assertIsNone(output)
        ellipse_coordinates = canvas.coords(ellipse.tag)
        self.assertListEqual(ellipse_coordinates, [50, 50, 400, 400])

    def test_function_resize_should_resize_2_shapes_if_2_selected(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).resize([rectangle, ellipse], [500, 500])
        self.assertIsNone(output)
        ellipse_coordinates = canvas.coords(ellipse.tag)
        rectangle_coordinates = canvas.coords(rectangle.tag)
        self.assertListEqual(ellipse_coordinates, [50, 50, 500, 500])
        self.assertListEqual(rectangle_coordinates, [300, 300, 500, 500])

    def test_function_group_with_no_shapes_should_return_false(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).group([])
        self.assertFalse(output)

    def test_function_group_with_shapes_should_return_group_object(self):
        canvas = Canvas()
        ellipse = self.create_ellipse(canvas, [50, 50, 100, 100])
        rectangle = self.create_rectangle(canvas, [300, 300, 400, 400])
        ellipse.draw()
        rectangle.draw()
        canvas.pack()
        output = Commands(canvas, [ellipse, rectangle]).group([ellipse, rectangle])
        self.assertIsInstance(output, Group)
        self.assertEqual(len(output.get_all()), 2)
        self.assertListEqual([ellipse, rectangle], output.get_all())


if __name__ == '__main__':
    unittest.main()
