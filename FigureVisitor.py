class FigureVisitor:
    """
    Used for the Visitor pattern
    """
    def __str__(self):
        return self.__class__.__name__
