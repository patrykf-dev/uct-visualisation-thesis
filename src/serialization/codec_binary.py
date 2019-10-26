import bitstring


def write_string(bin_list, string_content):
    bin_list.append(_encode_integer(len(string_content)))
    bin_list.append(_encode_string(string_content))


def write_integer(bin_list, value):
    bin_list.append(_encode_integer(value))


def write_float(bin_list, value):
    bin_list.append(_encode_float(value))


_INT_SIZE = 4
_FLOAT_SIZE = 8


def _encode_integer(value):
    return value.to_bytes(_INT_SIZE, byteorder="little")


def _encode_string(content):
    return content.encode("utf-8")


def _encode_float(value):
    # TODO: ensure it's written on 8 bytes, currently _FLOAT_SIZE not used
    value_bytes = bitstring.BitArray(floatle=value, length=64).tobytes()
    return value_bytes
