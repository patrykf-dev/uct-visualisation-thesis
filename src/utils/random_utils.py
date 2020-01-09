import random

random.seed(a=123456)


def get_random_int(value_from, value_to):
    """
    :param value_from: int
    :param value_to: int
    :return: random int from range [value_from, value_to]
    """
    span = value_to - value_from
    return int(span * random.random() + value_from)
