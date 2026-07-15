""" Calculate distance in bits between EUI-48 (a.k.a. 48-bit MAC) strings. """

from string import hexdigits
from typing import Iterable


EUI48_OCTETS = 48 // 8
EUI48_LENGTH = EUI48_OCTETS * 2 + (EUI48_OCTETS - 1)  # 17, string length
EUI48_MAX = 2 ** 48 - 1  # it's not a magic number if it's in the name


def check_eui48(a: str, /) -> bool:
    """ Check if input is a EUI-48 string.

    :return: ``True`` if `a` is a EUI-48 string, otherwise ``False``.
    """
    if len(a) != EUI48_LENGTH:
        return False
    isep = frozenset(range(2, EUI48_LENGTH, 3))
    for i, c in enumerate(a):
        if i in isep:
            if c != ':':
                return False
        elif c not in hexdigits:
            return False
    return True


def int_to_eui48(i: int, /) -> str:
    """ Convert int into EUI-48 string.

    :raises ValueError: If the provided value cannot be represented by EUI-48.
    :return: `i` converted from ``int`` into EUI-48 string.
    """
    if 0 <= i <= EUI48_MAX:
        return i.to_bytes(6, byteorder='big', signed=False).hex(':')
    raise ValueError('this number cannot be represented as EUI-48')


def eui48_to_int(a: str, /) -> int:
    """ Convert EUI-48 string into int.

    :return: `a` converted from EUI-48 string into ``int``.
    """
    octets = [int(s, 16) for s in a.split(':')]
    return int.from_bytes(octets, byteorder='big', signed=False)


def eui48_bit_distance(a: str, b: str, /) -> int:
    """ Calculate bit distance between two EUI-48 strings.

    :return: Amount of bits that are different between `a` and `b`.
    """
    ia = eui48_to_int(a)
    ib = eui48_to_int(b)
    return (ia ^ ib).bit_count()


def eui48_find_similar(a: str, iterable: Iterable[str], /, *, cutoff: int = 8) -> list[tuple[int, str]]:
    """ Return EUI-48 strings and their distances from reference EUI-48 string.

    This function measures and orders output by the distances between `a` and every string in `iterable`. To reduce the
    number of elements in the output, it also drops inputs that have distance greater than `cutoff`.

    :return: A list of 2-tuples ``(distance, EUI-48 string)``.
    """
    result = (
        (eui48_bit_distance(a, item), item)
        for item in iterable
    )
    return sorted([
        (dist, item)
        for (dist, item) in result
        if dist <= cutoff
    ])
