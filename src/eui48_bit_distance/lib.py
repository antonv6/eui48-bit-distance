""" Calculate distance in bits between EUI-48 (a.k.a. 48-bit MAC) strings. """

from collections.abc import Iterable
from itertools import islice
from string import hexdigits


EUI48_MAX = 2 ** 48 - 1


class EUI48Format:
    def __init__(self, example: str, sep: str) -> None:
        self.example = example
        self.sep = sep
        self.group = example.find(sep)
        self.length = len(example)
        self.isep = tuple(range(self.group, self.length, self.group + 1))
        self.idigit = tuple(i for i in range(self.length) if i not in self.isep)

        # itertools.batched() is only 3.12+
        iterator = iter(self.idigit)
        self.ipairs = tuple(tuple(islice(iterator, 2)) for _ in range(len(self.idigit) // 2))

    def match(self, a: str) -> bool:
        if len(a) != self.length:
            return False
        if not all(a[i] == self.sep for i in self.isep):
            return False
        if not all(a[i] in hexdigits for i in self.idigit):
            return False
        return True


EUI48_FORMATS = (
    EUI48Format('12:34:56:78:90:ab', ':'),
    EUI48Format('12-34-56-78-90-ab', '-'),
)


def check_eui48(a: str, /) -> bool:
    """ Check if the input is an EUI-48 identifier.

    Supported formats: ``12:34:56:78:90:ab``, ``12-34-56-78-90-ab`` and ``1234.5678.90ab``. Letters can be in upper or
    lower case.

    :return: ``True`` if `a` is an EUI-48 identifier, otherwise ``False``.
    """
    return any(fmt.match(a) for fmt in EUI48_FORMATS)


def int_to_eui48(i: int, /, *, sep: str = ':', group: int = 2) -> str:
    """ Convert an integer into an EUI-48 identifier.

    Supported formats: ``12:34:56:78:90:ab``, ``12-34-56-78-90-ab`` and ``1234.5678.90ab``. Set `sep` to either ':' (the
    default value), '-' or '.'.

    :raises ValueError: If the provided value cannot be represented by EUI-48.
    :return: `i` converted from ``int`` into EUI-48 identifier.
    """
    if 0 <= i <= EUI48_MAX:
        return i.to_bytes(6, byteorder='big', signed=False).hex(sep, bytes_per_sep=group // 2)
    raise ValueError(f'this number cannot be represented as EUI-48: {i!r}')


def eui48_to_int(a: str, /) -> int:
    """ Convert an EUI-48 identifier into an integer.

    Supported formats: ``12:34:56:78:90:ab``, ``12-34-56-78-90-ab`` and ``1234.5678.90ab``. Letters can be in upper or
    lower case.

    No checks are performed on the input: if the provided string is not an EUI-48 identifier, this function will produce
    an error. Use :func:`check_eui48` first if you're not sure about the input.

    :raises ValueError: If `a` cannot be parsed as EUI-48 identifier.
    :return: `a` converted from EUI-48 identifier into ``int``.
    """
    for fmt in EUI48_FORMATS:
        if fmt.match(a):
            octets = [int(a[i1] + a[i2], 16) for (i1, i2) in fmt.ipairs]
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
