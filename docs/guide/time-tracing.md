# Time Tracing

Enable timing with `time_trace=True`:

```python
from tracer import tracer

@tracer(trace_entity=True, time_trace=True)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 2) + fib(n - 1)

fib(3)
```

Each return line gains its own cost:

```text
-> fib(n=3)
|  -> fib(n=1)
|  |  <- fib returned 1 | cost=0.000012s
...
```

After the traced run finishes, a summary report is emitted:

```text
===== Function Trace Statistics Report =====
Function        Calls   Total(s)  Avg(s)    Min(s)    Max(s)
fib             5       0.0002    0.0000    0.0000    0.0001
============================================
```

The report is written through the same `output_way` pipeline as the trace
itself, so it can be sent to a file, a stream or multiple destinations.

## Report fields

| Column | Meaning |
| --- | --- |
| `Function` | Function name |
| `Calls` | Number of completed calls in the run |
| `Total(s)` | Accumulated wall-clock time |
| `Avg(s)` | Mean call duration |
| `Min(s)` / `Max(s)` | Fastest and slowest call |

Timing uses `time.perf_counter()` and is keyed by frame, so recursive calls are
measured individually.

## Scope

Statistics are reset at the beginning of each top-level run. Calling a decorated
function three times produces three independent reports, each covering one run.
The same applies to reusing a `Tracer` context manager.
