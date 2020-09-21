import Decorators.Description as Description


class Bottom(Description):

    _words = None

    def __init__(self, description, words):
        Description.__init__(self, description)
        self._words = words

    @staticmethod
    def position():
        return 'bottom'

    def get_description(self):
        return self.description.get_description() + ...[{self.position(): self._words}]