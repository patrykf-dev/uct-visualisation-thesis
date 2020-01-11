import numpy as np


def rational_function(x, a, b):
    return a / (x + b)


def expotential_function(x, a, b):
    return a * pow(b, x)


def normalize(v):
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm
