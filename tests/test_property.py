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
def test_eui48_roundtrip(a):
    assert eui48_to_int(int_to_eui48(a)) == a


@given(st.integers(0, EUI48_MAX), st.integers(0, 48))
def test_eui48_bit_distance(base, dist):
    mask = 2 ** dist - 1
    a = int_to_eui48(base)
    b = int_to_eui48(base ^ mask)
    assert eui48_bit_distance(a, b) == dist
