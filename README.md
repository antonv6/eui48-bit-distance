# eui48-bit-distance

[![Status: Beta](https://img.shields.io/pypi/status/eui48-bit-distance)](https://pypi.org/project/eui48-bit-distance/)
[![Release](https://img.shields.io/github/v/release/antonv6/eui48-bit-distance)](https://github.com/antonv6/eui48-bit-distance/releases)
[![PyPI](https://img.shields.io/pypi/v/eui48-bit-distance)](https://pypi.org/project/eui48-bit-distance/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/eui48-bit-distance)](https://pypi.org/project/eui48-bit-distance/)

[![License: Apache-2.0](https://img.shields.io/pypi/l/eui48-bit-distance)](https://github.com/antonv6/eui48-bit-distance/blob/main/LICENSE)
[![Codecov](https://codecov.io/github/antonv6/eui48-bit-distance/graph/badge.svg?token=QWGJX4C409)](https://codecov.io/github/antonv6/eui48-bit-distance)
[![CodeQL](https://github.com/antonv6/eui48-bit-distance/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/antonv6/eui48-bit-distance/actions/workflows/github-code-scanning/codeql)
[![Typed](https://img.shields.io/pypi/types/eui48-bit-distance)](https://pypi.org/project/eui48-bit-distance/)

*Calculate bit distance between EUI-48 (MAC).*

## Links

- **Docs:** https://antonv6.github.io/eui48-bit-distance/
- **Source:** https://github.com/antonv6/eui48-bit-distance
- **Issues:** https://github.com/antonv6/eui48-bit-distance/issues
- **Changelog:** https://github.com/antonv6/eui48-bit-distance/blob/main/CHANGELOG.md


## Developing locally

Installing dependencies (using `venv` and `pip`):

```bash
python -m venv .venv
.venv/bin/pip install --upgrade pip --uploaded-prior-to P7D
.venv/bin/pip install --group dev --uploaded-prior-to P7D
```

> [!TIP]
> You can also activate the virtual environment manually, or use something like
> `direnv` to do it automatically. The rest of the recipes here just keep
> showing the required path to run the commands.

Running all tests using the default local Python version:

```bash
.venv/bin/tox -e test
```

Running a subset of tests (see `tool.tox.env_base.test` config) across many
Pythons:

```bash
.venv/bin/tox run-parallel -m test
```

Running benchmarks across specific Pythons:

```bash
.venv/bin/tox -f 3.11 -f pypy3.11 -- tests/test_benchmark.py
```

Linting (targeting the default local Python version):

```bash
.venv/bin/tox -e lint
```

Building HTML documentation:

```bash
.venv/bin/tox -e docs
```

Building distribution files:

```bash
.venv/bin/tox -e build
```
