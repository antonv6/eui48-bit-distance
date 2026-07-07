""" Calculate distance in bits between EUI-48 (a.k.a. 48-bit MAC) strings. """

from string import hexdigits

EUI48_OCTETS = 48 // 8
EUI48_LENGTH = EUI48_OCTETS * 2 + (EUI48_OCTETS - 1)  # 17, string length
EUI48_MAX = 2 ** 48 - 1  # it's not a magic number if it's in the name


def check_eui48(a):
    """ Check if input is a EUI-48 string. """
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


def int_to_eui48(i):
    """ Convert int into EUI-48 string. """
    if 0 <= i <= EUI48_MAX:
        return i.to_bytes(6, byteorder='big', signed=False).hex(':')
    raise ValueError('this number cannot be represented as EUI-48')


def eui48_to_int(string):
    """ Convert EUI-48 string into int. """
    octets = [int(s, 16) for s in string.split(':')]
    return int.from_bytes(octets, byteorder='big', signed=False)


def eui48_bit_distance(a, b):
    """ Calculate bit distance between two EUI-48 strings. """
    ia = eui48_to_int(a)
    ib = eui48_to_int(b)
    return (ia ^ ib).bit_count()


def eui48_find_similar(a, iterable, cutoff=8):
    """ Return EUI-48 strings and their differences from reference EUI-48 string. """
    result = (
        (eui48_bit_distance(a, item), item)
        for item in iterable
    )
    return sorted([
        (dist, item)
        for (dist, item) in result
        if dist <= cutoff
    ])
