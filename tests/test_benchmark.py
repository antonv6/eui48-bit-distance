from src.eui48_bit_distance import (
    bytes_to_eui48,
    check_eui48,
    eui48_bit_distance,
    eui48_find_similar,
    eui48_to_bytes,
    eui48_to_int,
    int_to_eui48,
)


def test_bench_eui48_to_bytes(benchmark):
    benchmark(eui48_to_bytes, '12:34:56:78:90:ab')


def test_bench_eui48_to_int(benchmark):
    benchmark(eui48_to_int, '12:34:56:78:90:ab')


def test_bench_bytes_to_eui48(benchmark):
    benchmark(bytes_to_eui48, bytes([0x12, 0x34, 0x56, 0x78, 0x90, 0xab]))


def test_bench_int_to_eui48(benchmark):
    benchmark(int_to_eui48, 42)


def test_bench_check_eui48(benchmark):
    benchmark(check_eui48, '12:34:56:78:90:ab')


def test_bench_eui48_bit_distance(benchmark):
    benchmark(eui48_bit_distance, '12:34:56:78:90:ab', '12:34:56:78:90:ab')


def test_bench_eui48_find_similar(benchmark):
    benchmark(eui48_find_similar, '12:34:56:78:90:ab', [
        '00:00:00:00:00:00',
        '12:34:56:78:90:ab',
        'ff:ff:ff:ff:ff:ff',
    ])
