import random

random.seed(a=123456)


def get_random_int(int_from, int_to):
    return random.randint(int_from, int_to - 1)
