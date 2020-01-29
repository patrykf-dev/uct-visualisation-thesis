
class CustomEvent(object):
    """
    Class implements event mechanism.
    """
    def __init__(self):
        self.handlers = []

    def add(self, handler):
        """
		Args:
			handler:  function object

		Returns:
			add function to event queue        
		"""
        self.handlers.append(handler)
        return self

    def remove(self, handler):
        """
		Args:
			handler:  function object

		Returns:
			remove function from event queue        
		"""
        self.handlers.remove(handler)
        return self

    def fire(self, sender, earg=None):
        """
        For each handler in the event queue, execute it.

		Args:
			sender:  function that generates the event
			earg:  optional arguments that come with the raised event

		"""
        for handler in self.handlers:
            handler(sender, earg)

    __iadd__ = add
    __isub__ = remove
    __call__ = fire

