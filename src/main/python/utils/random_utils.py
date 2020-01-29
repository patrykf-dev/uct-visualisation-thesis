
import random


def get_random_int(value_from, value_to):
    """
		Args:
			value_from:  int
			value_to:  int

		Returns:
			random int from range [value_from, value_to]    
		"""
    span = value_to - value_from
    return int(span * random.random() + value_from)

