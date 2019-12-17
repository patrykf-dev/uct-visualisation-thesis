import struct


def write_string(bin_list, string_content):
    bin_list.append(_encode_integer(len(string_content)))
    bin_list.append(_encode_string(string_content))


def write_integer(bin_list, value):
    bin_list.append(_encode_integer(value))


def write_float(bin_list, value):
    bin_list.append(_encode_float(value))


def read_string(file):
    string_size = int.from_bytes(file.read(_INT_SIZE), byteorder=_BYTE_ORDER)
    return file.read(string_size).decode(_STRING_FORMAT)


def read_integer(file):
    return int.from_bytes(file.read(_INT_SIZE), byteorder=_BYTE_ORDER)


def read_float(file):
    content_bytes = file.read(_FLOAT_SIZE)
    return struct.unpack(_FLOAT_PACK_FORMAT, content_bytes)[0]


_INT_SIZE = 4
_FLOAT_SIZE = 8
_BYTE_ORDER = "little"
_STRING_FORMAT = "utf-8"
_FLOAT_PACK_FORMAT = "<d"


def _encode_integer(value):
    return value.to_bytes(_INT_SIZE, byteorder=_BYTE_ORDER)


def _encode_string(content):
    return content.encode(_STRING_FORMAT)


def _encode_float(value):
    return bytes(struct.pack(_FLOAT_PACK_FORMAT, value))
