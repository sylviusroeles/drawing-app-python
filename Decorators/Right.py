from Decorators.Description import Description


class Right(Description):

    _description = None

    def __init__(self, description):
        """
        :param description:
        """
        self._description = description

    def render(self):
        """
        :return:
        """
        return {"Right": self._description.render()}

    def to_string(self):
        """
        :return:
        """
        return "right \"%s\"" % self._description.render()