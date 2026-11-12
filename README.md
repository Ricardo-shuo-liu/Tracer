# Tracer

A lightweight, intrusive tracer for Python function calls.

[![PyPI](https://img.shields.io/pypi/v/pypi-tracer.svg)](https://pypi.org/project/pypi-tracer/)
[![Python](https://img.shields.io/pypi/pyversions/pypi-tracer.svg)](https://pypi.org/project/pypi-tracer/)
[![License](https://img.shields.io/github/license/Ricardo-shuo-liu/Tracer.svg)](LICENSE)

Tracer records the call tree of selected functions, reports per-function timing,
extracts exceptions with their full propagation path, and routes all output
through one configurable pipeline. It has no third-party runtime dependencies.

```python
from tracer import tracer

@tracer(trace_entity=True)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 2) + fib(n - 1)

fib(3)
```

```text
-> fib(n=3)
|  -> fib(n=1)
|  |  <- fib returned 1
|  -> fib(n=2)
|  |  -> fib(n=0)
|  |  |  <- fib returned 0
|  |  -> fib(n=1)
|  |  |  <- fib returned 1
|  |  <- fib returned 1
|  <- fib returned 2
```

## Features

- **Call tree** — hierarchical `->` / `<-` trace with arguments and return values.
- **Timing** — per-call cost and a per-function statistics report.
- **Exception analysis** — origin, full stack, propagation path, handled/escaped
  status, optional local snapshots and JSON export.
- **One output pipeline** — console, file paths, callables, writable streams or
  multiple destinations, controlled by `output_way` and `overwrite`.
- **Color on terminals only** — ANSI codes are never written to files.
- **No dependencies** — standard library only, Python 3.10.9+.

## Installation

```bash
pip install pypi-tracer
```

The distribution is named `pypi-tracer`; the import package is `tracer`.

From source:

```bash
git clone https://github.com/Ricardo-shuo-liu/Tracer.git
cd Tracer
pip install -e .
```

## Quick start

```python
from tracer import tracer

def add(x, y):
    return x + y

@tracer(trace_fn=[add], trace_entity=True)
def run():
    return add(1, 2)

run()
```

Use the context manager when you do not want to decorate the entry function:

```python
from tracer import Tracer

with Tracer(trace_fn=[add]):
    add(1, 2)
```

Send output to a file, a callable, a stream or several destinations:

```python
@tracer(trace_entity=True, output_way="trace.log", overwrite=True)
def run():
    ...
```

## Documentation

The full documentation lives in [`docs/`](docs/index.md):

- [Getting started](docs/getting-started.md)
- [Output redirection](docs/guide/output.md)
- [Time tracing](docs/guide/time-tracing.md)
- [Exception tracing](docs/guide/exception-tracing.md)
- [API reference](docs/api.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [Migration guide](docs/migration.md)

To build the documentation site locally:

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

Chinese documentation: [README_zh.md](README_zh.md) and [`docs/zh/`](docs/zh/index.md).

## Requirements

- Python 3.10.9 or newer.
- No third-party runtime dependencies.

## License

MIT. See [LICENSE](LICENSE).
