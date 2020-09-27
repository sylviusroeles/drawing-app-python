from Decorators.Description import Description


class Left(Description):

    _description = None

    def __init__(self, description):
        self._description = description

    def render(self):
        return {"Left": self._description.render()}