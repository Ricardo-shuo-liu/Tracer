# Tracer

**A lightweight, intrusive tracer for Python function calls.**

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
  status, optional local-variable snapshots and JSON export.
- **One output pipeline** — console, file paths, callables, writable streams or
  multiple destinations, all controlled by `output_way` and `overwrite`.
- **Color on terminals only** — ANSI codes are never written to file targets.
- **No dependencies** — standard library only, Python 3.10.9+.

## Installation

```bash
pip install pypi-tracer
```

The distribution is named `pypi-tracer`; the import package is `tracer`.

## Documentation

- [Getting started](getting-started.md)
- [Output redirection](guide/output.md)
- [Time tracing](guide/time-tracing.md)
- [Exception tracing](guide/exception-tracing.md)
- [API reference](api.md)
- [Architecture](architecture.md)

## License

MIT. See [LICENSE](https://github.com/Ricardo-shuo-liu/Tracer/blob/main/LICENSE).
