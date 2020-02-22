

class Figure:

    tag = None

    def __init__(self, canvas):
        """
        :param canvas:
        """
        self.canvas = canvas

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
