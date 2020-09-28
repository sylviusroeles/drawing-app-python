from Figure import *

class Group(Figure):

    descriptions = None

    def __init__(self, canvas):
        """
        :param canvas:
        """
        super().__init__(None, canvas, 'group', None)
        self.shapes = []

    def add(self, shape):
        """
        :param shape:
        :return:
        """
        self.shapes.append(shape)

    def remove(self, shape):
        """
        :param shape:
        :return:
        """
        self.shapes.remove(shape)

    def get_all(self):
        """
        :return:
        """
        return self.shapes

    def draw(self):
        """
        :return:
        """
        for shape in self.shapes:
            shape.draw()

    def render_description(self):
        """
        :return:
        """
        for description in self.descriptions:

            for position in description.render():

                # get the middle of the shapes in the group
                x1 = sum([shape.coordinates[X1] for shape in self.shapes]) / len(self.shapes)
                y1 = sum([shape.coordinates[Y1] for shape in self.shapes]) / len(self.shapes)
                x2 = sum([shape.coordinates[X2] for shape in self.shapes]) / len(self.shapes)
                y2 = sum([shape.coordinates[Y2] for shape in self.shapes]) / len(self.shapes)

                if position == "Bottom":
                    y2 = max([shape.coordinates[Y2] for shape in self.shapes])
                if position == "Top":
                    y1 = min([shape.coordinates[Y1] for shape in self.shapes])
                if position == "Right":
                    x2 = max([shape.coordinates[X2] for shape in self.shapes])
                if position == "Left":
                    x1 = min([shape.coordinates[X1] for shape in self.shapes])

                coordinates = [
                    x1, y1, x2, y2
                ]

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