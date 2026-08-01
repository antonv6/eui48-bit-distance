from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize('src/eui48_bit_distance/lib.py', annotate=True),
)
