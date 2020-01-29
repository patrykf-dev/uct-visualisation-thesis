
import numpy as np


def rational_function(x, a, b):
    """
		Args:
			x:  numeric value
			a:  numeric value
			b:  numeric value

		Returns:
			rational function value: y = a / (x + b)    
		"""
    return a / (x + b)


def expotential_function(x, a, b):
    """
		Args:
			x:  numeric value
			a:  numeric value
			b:  numeric value

		Returns:
			exponential function value: y = a * b^x    
		"""
    return a * pow(b, x)


def normalize(v):
    """
		Args:
			v:  numpy vector

		Returns:
			normalized numpy vector    
		"""
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm

