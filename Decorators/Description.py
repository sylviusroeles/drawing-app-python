from tkinter import W

class Description(object):

    _description = None
    _canvas = None

    def __init__(self, description, canvas):
        """
        :param description:
        """
        self._description = description
        self._canvas = canvas

    def get_description(self):
        """
        :return:
        """
        return self._description

    def render(self):
        """
        :return:
        """
        return self._description