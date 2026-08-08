""" Calculate distance in bits between EUI-48 (a.k.a. 48-bit MAC) strings. """

import re
from collections.abc import Iterable


EUI48_MAX = 2 ** 48 - 1  # it's not a magic number if it's in the name
EUI48_RE = (
    # 12:34:56:78:90:ab
    re.compile(':'.join(['([0-9A-Fa-f]{2})'] * 6)),
    # 12-34-56-78-90-ab
    re.compile('-'.join(['([0-9A-Fa-f]{2})'] * 6)),
)


def check_eui48(a: str, /) -> bool:
    """ Check if the input is an EUI-48 identifier.

    Supported formats: ``12:34:56:78:90:ab`` and ``12-34-56-78-90-ab``. Letters can be in upper or lower case.

    :return: ``True`` if `a` is an EUI-48 identifier, otherwise ``False``.
    """
    for regex in EUI48_RE:
        if regex.fullmatch(a) is not None:
            return True
    return False


def int_to_eui48(i: int, /, *, sep: str = ':') -> str:
    """ Convert an integer into an EUI-48 identifier.

    Supported formats: ``12:34:56:78:90:ab`` and ``12-34-56-78-90-ab``. Set `sep` to either ':' (the default value) or
    '-'.

    :raises ValueError: If `i` cannot be represented by EUI-48.
    :return: `i` converted from ``int`` into EUI-48 identifier.
    """
    if 0 <= i <= EUI48_MAX:
        return i.to_bytes(6, byteorder='big', signed=False).hex(sep)
    raise ValueError(f'this number cannot be represented as EUI-48: {i!r}')


def eui48_to_int(a: str, /) -> int:
    """ Convert an EUI-48 identifier into an integer.

    Supported formats: ``12:34:56:78:90:ab`` and ``12-34-56-78-90-ab``. Letters can be in either upper or lower case.

    :func:`check_eui48` can be used to check if the input is a valid EUI-48 identifier.

    :raises ValueError: If `a` cannot be parsed as EUI-48 identifier.
    :return: `a` converted from EUI-48 identifier into ``int``.
    """
    for regex in EUI48_RE:
        match = regex.fullmatch(a)
        if match is not None:
            octets = [int(g, 16) for g in match.groups()]
            return int.from_bytes(octets, byteorder='big', signed=False)
    raise ValueError(f'invalid EUI-48: {a!r}')


def eui48_bit_distance(a: str, b: str, /) -> int:
    """ Calculate bit distance between two EUI-48 identifiers.

    :return: The amount of bits that are different between `a` and `b`.
    """
    ia = eui48_to_int(a)
    ib = eui48_to_int(b)
    return (ia ^ ib).bit_count()


def eui48_find_similar(a: str, iterable: Iterable[str], /, *, cutoff: int = 8) -> list[tuple[int, str]]:
    """ Return EUI-48 identifiers and their distances from the reference EUI-48 identifier.

    This function measures and orders output by the distances between `a` and every string in `iterable`. To reduce the
    number of elements in the output, it also drops inputs that have distance greater than `cutoff`.

    :return: A list of 2-tuples ``(distance, EUI-48 identifier)``.
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
