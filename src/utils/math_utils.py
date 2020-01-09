import numpy as np


def rational_function(x, a, b):
    """
    :param x: numeric value
    :param a: numeric value
    :param b: numeric value
    :return: rational function value: y = a / (x + b)
    """
    return a / (x + b)


def expotential_function(x, a, b):
    """
    :param x: numeric value
    :param a: numeric value
    :param b: numeric value
    :return: exponential function value: y = a * b^x
    """
    return a * pow(b, x)


def normalize(v):
    """
    :param v: numpy vector
    :return: normalized numpy vector
    """
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm
