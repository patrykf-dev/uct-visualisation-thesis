import numpy as np


def get_2d_array_deep_copy(ref_array):
    """
    :param ref_array: array to be copied
    :return: deep copy of given array
    """
    return ref_array.copy()


def generate_2d_zeros_array(width, height):
    """
    :param width: int
    :param height: int
    :return: numpy zero matrix of given size: width*height
    """
    return np.zeros(shape=(width, height), dtype=int)


def generate_2d_nones_array(width, height):
    """
    :param width: int
    :param height: int
    :return: numpy matrix filled with Nones of given size: width*height
    """
    return np.full((width, height), None)
