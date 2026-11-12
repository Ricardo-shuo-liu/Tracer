# Exception Tracing

Exception tracing observes every exception raised inside the traced scope and
emits a structured report after the run. It never swallows or suppresses an
exception: the original exception keeps propagating exactly as before.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `exception_trace` | `False` | Master switch for exception analysis |
| `show_locals` | `False` | Snapshot local variables where the exception is first observed |
| `exception_json_path` | `None` | Write all records to this JSON file after the run |

## Example

```python
from tracer import tracer

def deep_untraced(n):          # not listed in trace_fn
    if n < 0:
        raise ValueError(f"negative depth: {n}")
    return n * 2

def risky(n):
    return deep_untraced(n)

def swallowed():
    try:
        raise KeyError("swallowed_key")
    except KeyError:
        return "recovered"

@tracer(
    trace_fn=[risky, swallowed],
    trace_entity=True,
    exception_trace=True,
    show_locals=True,
)
def run():
    swallowed()
    return risky(-1)

try:
    run()
except ValueError:
    pass
```

The trace marks unwinding frames with `raised` instead of `returned`:

```text
-> run()
|  -> swallowed()
|  |  <- swallowed returned 'recovered'
|  -> risky(n=-1)
|  |  <- risky raised ValueError: negative depth: -1
|  <- run raised ValueError: negative depth: -1
```

The report follows:

```text
===== Exception Trace Report =====
total=2  unhandled=1  handled=1  by_type={'KeyError': 1, 'ValueError': 1}
----------------------------------
#1  KeyError: 'swallowed_key'
    status      : handled by swallowed()
    raised at   : swallowed() -> demo.py:13
    propagated  : swallowed
    stack (outermost -> raise point):
      File "demo.py", line 13, in swallowed
        raise KeyError("swallowed_key")
----------------------------------
#2  ValueError: negative depth: -1
    status      : escaped (unhandled within traced scope)
    raised at   : deep_untraced() -> demo.py:5
    propagated  : risky -> run
    stack (outermost -> raise point):
      File "demo.py", line 20, in run
        return risky(-1)
      File "demo.py", line 8, in risky
        return deep_untraced(n)
      File "demo.py", line 5, in deep_untraced
        raise ValueError(f"negative depth: {n}")
    locals at observation point:
      n = -1
----------------------------------
==================================
```

## Captured fields

| Field | Meaning |
| --- | --- |
| `exc_type` / `message` | Exception class name and `str()` of the instance |
| `raised at` | Function, file and line where the exception originated |
| `stack` | Full traceback, including frames that were never traced |
| `propagated` | Traced functions the exception travelled through, e.g. `dive x4 -> safe` |
| `status` | `handled by fn()` when swallowed inside the scope, `escaped` otherwise |
| `locals` | Local snapshot at the observation point (`show_locals=True`) |

## Programmatic access

```python
with Tracer(trace_fn=[dive], exception_trace=True) as t:
    ...

t.errors.records      # list[ExcRecord]
t.errors.to_list()    # list[dict], JSON-serialisable
t.errors.unhandled    # exceptions that escaped the traced scope
t.errors.handled      # exceptions swallowed inside the traced scope
```

With the decorator, the context is attached to the wrapper:

```python
@tracer(trace_entity=True, exception_trace=True)
def run(): ...

run()
run.tracer_ctx.errors.to_list()
```

## JSON format

`exception_json_path` writes a document with this shape:

```json
{
  "summary": {
    "total": 2,
    "unhandled": 1,
    "handled": 1,
    "by_type": {"KeyError": 1, "ValueError": 1}
  },
  "exceptions": [
    {
      "seq": 1,
      "exc_type": "KeyError",
      "message": "'swallowed_key'",
      "status": "handled by swallowed()",
      "raised_at": {"func_name": "swallowed", "filename": "demo.py", "lineno": 13, "code_line": "raise KeyError(\"swallowed_key\")"},
      "handled_by": "swallowed",
      "escaped": false,
      "propagation_path": ["swallowed"],
      "stack": [],
      "locals": {}
    }
  ]
}
```

The JSON file is written directly, not through `output_way`. If writing fails,
Tracer prints a warning to `stderr` and the original exception is not masked.

## Scope

Exceptions are observed only in frames that match the trace set (`trace_entity`
or `trace_fn`). Frames outside the set still appear in the traceback stack, but
are not independently traced.
