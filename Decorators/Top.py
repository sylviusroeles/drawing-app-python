from Decorators.Description import Description


class Top(Description):

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
        return {"Top": self._description.render()}

    def to_string(self):
        """
        :return:
        """
        return "top \"%s\"" % self._description.render()