from Decorators.Description import Description


class Right(Description):

    _description = None

    def __init__(self, description):
        self._description = description

    def render(self):
        return {"Right": self._description.render()}