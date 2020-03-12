from Strategy import *


class Figure:
    def __init__(self, canvas):
        """
        :param canvas:
        """
        self.canvas = canvas

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
            coordinates[0] - self.coordinates[0],
            coordinates[1] - self.coordinates[1]
        )
        self.coordinates[0] = coordinates[0]
        self.coordinates[1] = coordinates[1]

    def draw(self):
        Strategy(self.name, self.draw()).execute()

    def resize(self, visitor):
        """
        :param visitor:
        :return:
        """
        coordinates = visitor.coordinates
        self.canvas.coords(self.tag, coordinates[0], coordinates[1], coordinates[2], coordinates[3])

    @staticmethod
    def parse_coordinates(coordinates):
        """
        :param coordinates:
        :return:
        """
        return [
            coordinates[0],
            coordinates[1],
            str(int(coordinates[2]) - int(coordinates[0])),
            str(int(coordinates[3]) - int(coordinates[1])),
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
            ' '.join(coordinates)
        )
