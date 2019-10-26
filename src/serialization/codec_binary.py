import bitstring


def write_string(bin_list, string_content):
    bin_list.append(_encode_integer(len(string_content)))
    bin_list.append(_encode_string(string_content))


def write_integer(bin_list, value):
    bin_list.append(_encode_integer(value))


def write_float(bin_list, value):
    bin_list.append(_encode_float(value))


def read_string(file):
    string_size = _decode_integer(file)
    content = _decode_string(file, string_size)
    return content


def read_integer(file):
    return _decode_integer(file)


def read_float(file):
    return _decode_float(file)


_INT_SIZE = 4
_FLOAT_SIZE = 8


def _encode_integer(value):
    return value.to_bytes(_INT_SIZE, byteorder="little")


def _encode_string(content):
    return content.encode("utf-8")


def _encode_float(value):
    value_bytes = bitstring.BitArray(floatle=value, length=64).tobytes()
    return value_bytes


def _decode_integer(file):
    return int.from_bytes(file.read(_INT_SIZE), byteorder="little")


def _decode_string(file, length):
    return file.read(length).decode("utf-8")


def _decode_float(file):
    content_bytes = file.read(_FLOAT_SIZE)
    # TODO: ensure we decode it 64-based
    return bitstring.BitArray(content_bytes).floatle
