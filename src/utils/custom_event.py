class CustomEvent(object):
    """
    Class implements event mechanism.
    """

    def __init__(self):
        self.handlers = []

    def add(self, handler):
        """
        :param handler: function object
        :return: add function to event queue
        """
        self.handlers.append(handler)
        return self

    def remove(self, handler):
        """
        :param handler: function object
        :return: remove function from event queue
        """
        self.handlers.remove(handler)
        return self

    def fire(self, sender, earg=None):
        """
        For each handler in the event queue, execute it.
        :param sender: function that generates the event
        :param earg: optional arguments that come with the raised event
        :return:
        """
        for handler in self.handlers:
            handler(sender, earg)

    __iadd__ = add
    __isub__ = remove
    __call__ = fire
