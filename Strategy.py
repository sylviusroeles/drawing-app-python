import abc

class Strategy(object):
    """
    https://www.geeksforgeeks.org/strategy-method-python-design-patterns/
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, shape):
        """
        Master method
        :return:
        """

class RectangleStrategy(Strategy):
    """
    Rectangle drawing strategy
    """
    def execute(self, shape):
        return shape.draw()

class EllipseStrategy(Strategy):
    """
    Ellipse drawing strategy
    """
    def execute(self, shape):
        return shape.draw()