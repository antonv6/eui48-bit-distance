""" Calculate distance in bits between EUI-48 (a.k.a. 48-bit MAC) strings. """

from .lib import (
    EUI48_MAX,
    check_eui48,
    eui48_bit_distance,
    eui48_find_similar,
    eui48_to_int,
    int_to_eui48,
)


__all__ = [
    'EUI48_MAX',
    'check_eui48',
    'eui48_bit_distance',
    'eui48_find_similar',
    'eui48_to_int',
    'int_to_eui48',
]
