
class Description(object):

    _description = None

    def __init__(self, description):
        """
        :param description:
        """
        self._description = description

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

    def to_string(self):
        """
        :return:
        """
        return self.to_string()