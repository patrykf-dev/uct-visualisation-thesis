import numpy as np


def get_2d_array_deep_copy(ref_array):
    return ref_array.copy()


def generate_2d_zeros_array(width, height):
    return np.zeros(shape=(width, height), dtype=int)


def generate_2d_nones_array(width, height):
    return np.full((width, height), None)
