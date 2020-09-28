from Decorators.Description import Description


class Bottom(Description):

    _description = None

    def __init__(self, description):
        self._description = description

    def render(self):
        return {"Bottom": self._description.render()}

    def to_string(self):
        """
        :return:
        """
        return "bottom \"%s\"" % self._description.render()