def get_2d_array_deep_copy(ref_array):
    return [[x for x in row] for row in ref_array]


def generate_2d_zeros_array(width, height):
    return [[0] * width] * height


def generate_2d_nones_array(width, height):
    return [[None] * width for i1 in range(height)]
