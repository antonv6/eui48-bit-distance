# Changelog


## 0.3.2 - 2026-07-24

Various improvements to the development process, CI and security-related
improvements.

Improve HTML documentation, include README.md and CHANGELOG.md as well.


## 0.3.1 - 2026-07-18

Support Python 3.14.

Various improvements on the development side, especially tightening CI and
release security.


## 0.3.0 - 2026-07-17

Use `tox` to run linters, build documentation and distribution files, and test
locally with different Python versions.


## 0.2.5 - 2026-07-16

Build HTML documentation from docstrings using Sphinx with autodoc extension.

Deploy documentation to gh-pages.


## 0.2.4 - 2026-07-14

Use more PEP 570 positional-only parameters and keyword-only parameters.

We're breaking the API somewhat at this moment to make it easier to implement
speedup extensions in future.


## 0.2.3 - 2026-07-13

Benchmark performance with `pytest-benchmark`.


## 0.2.2 - 2026-07-12

Measure test coverage using `pytest-cov` and `coverage`.


## 0.2.1 - 2026-07-11

Property-based testing using Hypothesis.


## 0.2.0 - 2026-07-10

Add type hints to the code, checked with `mypy` in strict mode.


## 0.1.2 - 2026-07-09

Lint the code with `bandit`, `flake8` with extra plugins and `pylint`.


## 0.1.1 - 2026-07-08

Write docstrings and add CHANGELOG.md.


## 0.1.0 - 2026-07-07

Base functionality implemented.
