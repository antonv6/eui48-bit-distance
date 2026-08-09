from hypothesis import given, strategies as st

from src.eui48_bit_distance import (
    EUI48_MAX,
    check_eui48,
    eui48_bit_distance,
    eui48_to_int,
    int_to_eui48,
)


@given(st.integers(0, EUI48_MAX))
def test_generate_valid_eui48(a):
    assert check_eui48(int_to_eui48(a)) is True


@given(st.integers(0, EUI48_MAX))
def test_eui48_roundtrip_colon(a):
    assert eui48_to_int(int_to_eui48(a, sep=':')) == a


@given(st.integers(0, EUI48_MAX))
def test_eui48_roundtrip_hyphen(a):
    assert eui48_to_int(int_to_eui48(a, sep='-')) == a


@given(st.integers(0, EUI48_MAX))
def test_eui48_roundtrip_dot(a):
    assert eui48_to_int(int_to_eui48(a, sep='.', group=4)) == a


@given(st.integers(0, EUI48_MAX))
def test_eui48_case_colon(a):
    eui48 = int_to_eui48(a, sep=':')
    assert eui48_to_int(eui48.lower()) == eui48_to_int(eui48.upper())


@given(st.integers(0, EUI48_MAX))
def test_eui48_case_hyphen(a):
    eui48 = int_to_eui48(a, sep='-')
    assert eui48_to_int(eui48.lower()) == eui48_to_int(eui48.upper())


@given(st.integers(0, EUI48_MAX))
def test_eui48_case_dot(a):
    eui48 = int_to_eui48(a, sep='.', group=4)
    assert eui48_to_int(eui48.lower()) == eui48_to_int(eui48.upper())


@given(st.integers(0, EUI48_MAX))
def test_eui48_formats_colon_hyphen(a):
    assert eui48_to_int(int_to_eui48(a, sep=':')) == eui48_to_int(int_to_eui48(a, sep='-'))


@given(st.integers(0, EUI48_MAX))
def test_eui48_formats_colon_dot(a):
    assert eui48_to_int(int_to_eui48(a, sep=':')) == eui48_to_int(int_to_eui48(a, sep='.', group=4))


@given(st.integers(0, EUI48_MAX))
def test_eui48_formats_hyphen_dot(a):
    assert eui48_to_int(int_to_eui48(a, sep='-')) == eui48_to_int(int_to_eui48(a, sep='.', group=4))


@given(st.integers(0, EUI48_MAX), st.integers(0, 48))
def test_eui48_bit_distance(base, dist):
    mask = 2 ** dist - 1
    a = int_to_eui48(base)
    b = int_to_eui48(base ^ mask)
    assert eui48_bit_distance(a, b) == dist
