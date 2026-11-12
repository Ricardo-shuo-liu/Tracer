# Getting Started

## Requirements

- Python 3.10.9 or newer.
- No third-party runtime dependencies.

## Installation

From PyPI:

```bash
pip install pypi-tracer
```

From source:

```bash
git clone https://github.com/Ricardo-shuo-liu/Tracer.git
cd Tracer
pip install -e .
```

The distribution name is `pypi-tracer`; import it as `tracer`.

## Trace a function

```python
from tracer import tracer

def add(x, y):
    return x + y

@tracer(trace_fn=[add], trace_entity=True)
def run():
    return add(1, 2)

run()
```

Output:

```text
-> run()
|  -> add(x=1, y=2)
|  |  <- add returned 3
|  <- run returned 3
```

`trace_entity=True` traces the decorated function itself. `trace_fn=[...]` adds
the listed functions to the trace set.

## Use the context manager

`Tracer` avoids decorating the entry function:

```python
from tracer import Tracer

def add(x, y):
    return x + y

with Tracer(trace_fn=[add]):
    add(1, 2)
```

The context manager has no `trace_entity` parameter; list every function you
want to trace in `trace_fn`.

## Choose what is traced

Tracer matches frames by function **name**:

- `trace_entity=True` adds the decorated function's `__name__`.
- `trace_fn=[f, g]` adds `f.__name__` and `g.__name__`.
- If neither is provided, the trace set is unbounded and every frame executed
  while the hook is active is traced. See [Limitations](limitations.md).

## Configure output

By default output is written to the console (`stderr`). Pass any supported
destination through `output_way`:

```python
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

`output_way` also accepts callables, writable streams and lists of destinations.
See [Output Redirection](guide/output.md) for the complete matrix.

## Next steps

- [Output Redirection](guide/output.md)
- [Time Tracing](guide/time-tracing.md)
- [Exception Tracing](guide/exception-tracing.md)
- [Color](guide/color.md)
- [API Reference](api.md)
