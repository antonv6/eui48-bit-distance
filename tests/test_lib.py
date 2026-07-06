import pytest

from src.eui48_bit_distance import (
    EUI48_MAX,
    check_eui48,
    eui48_bit_distance,
    eui48_find_similar,
    eui48_to_int,
    int_to_eui48,
)


@pytest.mark.parametrize('a, b', [
    (0, '00:00:00:00:00:00'),
    (256, '00:00:00:00:01:00'),
    (EUI48_MAX, 'ff:ff:ff:ff:ff:ff'),
])
def test_int_to_eui48(a, b):
    assert int_to_eui48(a) == b


@pytest.mark.parametrize('a', [
    -1,
    EUI48_MAX + 1,
])
def test_int_to_eui48_invalid(a):
    with pytest.raises(ValueError):
        assert int_to_eui48(a) is not None


@pytest.mark.parametrize('a, b', [
    ('00:00:00:00:00:00', 0),
    ('00:00:00:00:01:00', 256),
    ('ff:ff:ff:ff:ff:ff', EUI48_MAX),
])
def test_eui48_to_int(a, b):
    assert eui48_to_int(a) == b


@pytest.mark.parametrize('a', [
    '00:00:00:00:00:00',
    '12:34:56:78:90:ab',
    'ab:cd:ef:ab:cd:ef',
    '1a:2b:3c:4d:5e:6f',
])
def test_check_eui48_true(a):
    assert check_eui48(a) is True


@pytest.mark.parametrize('a', [
    '00-00-00-00-00-00',
    'xx:xx:xx:xx:xx:xx',
    '00a00b00c00d00e00',
    '123456:::::7890ab',
    '1234567890ab',
    'ca:fe',
])
def test_check_eui48_false(a):
    assert check_eui48(a) is False


@pytest.mark.parametrize('a, b, distance', [
    # identical
    ('00:00:00:00:00:00', '00:00:00:00:00:00', 0),
    ('12:34:56:78:90:ab', '12:34:56:78:90:ab', 0),
    ('AB:CD:EF:01:23:45', 'ab:cd:ef:01:23:45', 0),

    # near
    ('00:00:00:00:00:00', '00:04:00:00:04:00', 2),
    ('00:00:00:00:00:00', '00:00:00:01:01:01', 3),

    # far
    ('ff:ff:ff:00:00:00', '00:00:00:FF:FF:FF', 48),
])
def test_eui48_bit_distance(a, b, distance):
    assert eui48_bit_distance(a, b) == distance


@pytest.mark.parametrize('a, b, distance', [
    (int_to_eui48(0b00000000), int_to_eui48(0b00000000), 0),
    (int_to_eui48(0b00000000), int_to_eui48(0b00000011), 2),
    (int_to_eui48(0b00000000), int_to_eui48(0b00111000), 3),
    (int_to_eui48(0b00110011), int_to_eui48(0b11001100), 8),
])
def test_eui48_bit_distance_manual_bits(a, b, distance):
    assert eui48_bit_distance(a, b) == distance


@pytest.mark.parametrize('a, iterable, cutoff, result', [
    # sanity checks
    ('00:00:00:00:00:00', [], 0, []),
    ('00:00:00:00:00:00', ['ff:ff:ff:ff:ff:ff'], 1, []),

    # basics
    ('00:00:00:00:00:00', ['00:00:00:00:00:00'], 16, [(0, '00:00:00:00:00:00')]),
    ('00:00:00:00:00:00', ['00:04:00:00:04:00'], 2, [(2, '00:04:00:00:04:00')]),

    # order and cutoff
    ('00:00:00:00:00:00', ['00:04:00:00:04:00',
                           '00:06:00:00:06:00'], 2, [(2, '00:04:00:00:04:00')]),
    ('00:00:00:00:00:00', ['00:04:00:00:04:00',
                           '00:06:00:00:06:00'], 4, [(2, '00:04:00:00:04:00'),
                                                     (4, '00:06:00:00:06:00')]),
])
def test_eui48_find_similar(a, iterable, cutoff, result):
    assert eui48_find_similar(a, iterable, cutoff=cutoff) == result


def test_eui48_find_similar_manual_bits():
    a = '00:00:00:00:00:00'
    iterable = [
        '00:00:00:00:00:01',
        '00:00:00:00:00:03',
        '00:00:00:00:00:07',
        '00:00:00:00:00:0f',
        '00:00:00:00:00:1f',
        '00:00:00:00:00:3f',
        '00:00:00:00:00:7f',
        '00:00:00:00:00:ff',
    ]
    assert eui48_find_similar(a, iterable) == [
        (1, '00:00:00:00:00:01'),
        (2, '00:00:00:00:00:03'),
        (3, '00:00:00:00:00:07'),
        (4, '00:00:00:00:00:0f'),
        (5, '00:00:00:00:00:1f'),
        (6, '00:00:00:00:00:3f'),
        (7, '00:00:00:00:00:7f'),
        (8, '00:00:00:00:00:ff'),
    ]


def test_eui48_find_similar_prepared():
    a = int_to_eui48(0)
    # 16 items from ...:00:01 to ...:ff:ff
    orig = [
        int_to_eui48(2 ** i - 1)
        for i in range(1, 17)
    ]
    assert len(orig) == 16
    # reverse the list before passing it to eui48_find_similar()
    iterable = orig[::-1]
    # cutoff is at 8 bits of difference, so up to ...:00:ff
    result = eui48_find_similar(a, iterable, cutoff=8)
    # we expect 8 items, in the original order, with difference of 1 through 8
    expected = list(enumerate(orig[:8], 1))
    assert result == expected
