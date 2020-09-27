import abc

class Strategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, shape):
        """
        Master method
        :return:
        """

class RectangleStrategy(Strategy):

    def execute(self, shape):
        return shape.draw()

class EllipseStrategy(Strategy):

    def execute(self, shape):
        return shape.draw()