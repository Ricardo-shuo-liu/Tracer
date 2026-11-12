# Architecture

## Module map

| Module | Responsibility |
| --- | --- |
| `tracer/core/Tracer.py` | Public `tracer` decorator and `Tracer` context manager |
| `tracer/core/TraceContext.py` | Per-run state: output buffer, timing, exception records |
| `tracer/core/Parser.py` | `sys.settrace` callback; formats call/return/exception events |
| `tracer/core/TraceStats.py` | Per-function timing aggregation and report |
| `tracer/core/Color.py` | Terminal capability detection and ANSI helpers |
| `tracer/exceptions/TraceError.py` | Exception records, reports and JSON export |
| `tracer/writer/` | Output normalization, fan-out and per-target writers |

## Data flow

```text
@tracer(...) / Tracer(...)
        │
        ├── normalize_output_way(output_way)
        │          └── WorkFlow ──► Writer[] ──► FileWriter / stream / callable
        │
        └── TraceContext ──► sys.settrace(hook)
                                  │
                      Parser.frame_callback
                         ├── call    → "-> fn(args)"
                         ├── return  → "<- fn returned value"
                         └── exception → TraceErrors.observe()
                                  │
                            TraceContext.add()
                                  │
                         finish() → WorkFlow.forward()
```

## Design decisions

### One normalization point

`normalize_output_way()` classifies the public `output_way` value exactly once.
It distinguishes single destinations (`None`, paths, callables, writable
streams) from collections, so iterable values such as `str`, `bytes` and
`StringIO` are not split into per-character or per-line destinations.

### Fan-out with isolation

`WorkFlow.forward()` writes each chunk to every `Writer`. A failing destination
does not prevent the remaining destinations from receiving output. The first
failure is re-raised to the emitter, which converts it into a warning on
`stderr` so that an output error cannot mask an exception escaping the traced
code.

### Per-run reset

`TraceContext.begin_run()` clears buffered lines, timing data, exception records
and pending exception frames at the start of every top-level run. Reports
therefore describe the run that just finished rather than accumulating across
calls.

### Hook restoration

The decorator and context manager save `sys.gettrace()` before installing their
hook and restore it afterwards. This keeps nested tracers, debuggers, coverage
tools and profilers working.

### Safe formatting

Argument and return values are formatted with a protected `repr()`. An object
whose `__repr__` raises is rendered as a placeholder instead of aborting the
traced call.

### Color policy

ANSI codes are enabled only when every destination is console-like. Because the
text is colorized before fan-out, this prevents escape sequences from leaking
into files.

## Threading

`sys.settrace` is thread-local. Only the thread that enters the decorator or the
`with` block is traced; other threads run without the hook.
