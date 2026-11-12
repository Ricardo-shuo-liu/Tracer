# API Reference

## `tracer`

```python
from tracer import tracer

tracer(
    trace_fn: list[Callable] | None = None,
    trace_entity: bool = False,
    output_way=None,
    overwrite: bool = False,
    time_trace: bool = False,
    use_color: bool = False,
    exception_trace: bool = False,
    show_locals: bool = False,
    exception_json_path: str | None = None,
) -> Callable
```

Decorator factory. Returns a decorator that wraps the target function.

| Parameter | Default | Description |
| --- | --- | --- |
| `trace_fn` | `None` | Additional functions to trace, matched by `__name__` |
| `trace_entity` | `False` | Trace the decorated function itself |
| `output_way` | `None` | Output destination; see [Output Redirection](guide/output.md) |
| `overwrite` | `False` | Truncate file destinations on first write |
| `time_trace` | `False` | Enable per-call timing and the statistics report |
| `use_color` | `False` | Enable ANSI color on console-like destinations |
| `exception_trace` | `False` | Enable exception collection and reporting |
| `show_locals` | `False` | Snapshot locals where an exception is observed |
| `exception_json_path` | `None` | Export exception records to this JSON file |

The wrapped function exposes the live context as `wrapped.tracer_ctx`.

If `trace_entity` is false and `trace_fn` is `None`, the trace set is unbounded
and every frame executed while the hook is active is traced.

## `Tracer`

```python
from tracer import Tracer

Tracer(
    trace_fn: list[Callable] | None = None,
    output_way=None,
    overwrite: bool = False,
    time_trace: bool = False,
    use_color: bool = False,
    exception_trace: bool = False,
    show_locals: bool = False,
    exception_json_path: str | None = None,
)
```

Context manager with the same configuration options as the decorator, except
`trace_entity`. List every function to trace in `trace_fn`.

| Member | Description |
| --- | --- |
| `with Tracer(...) as t:` | Installs the trace hook and returns the instance |
| `t.errors` | `TraceErrors` collector, or `None` when `exception_trace=False` |
| `t.stats` | `TraceStats` collector, or `None` when `time_trace=False` |

## Output target types

`output_way` accepts:

- `None` — console (`sys.stderr`).
- `str`, `bytes`, `os.PathLike` — UTF-8 file output.
- A callable — invoked with each output chunk.
- An object with `write()` — written to directly.
- An iterable of the above — fan-out output.

Invalid types raise `TypeError` when the decorator or context manager is created.
`overwrite=True` without any file destination raises `ValueError`.

## Run lifecycle

For each top-level invocation (decorator) or `with` block (context manager):

1. Per-run state is reset (timing, exception records, buffered lines).
2. `sys.settrace` is installed, saving the previously active hook.
3. Trace lines are buffered.
4. The previous hook is restored.
5. Buffered lines, exception report and timing report are written through
   `output_way`.

The decorated function's own recursion is tracked with an internal depth counter,
so nested calls do not reset the run or reinstall the hook.

## Public collectors

### `TraceStats`

| Member | Description |
| --- | --- |
| `data` | `dict[str, FuncStat]` keyed by function name |
| `format_report(setcolor=False)` | Return the statistics report as a string |
| `print_report(setcolor=False)` | Print the report to stdout |

### `TraceErrors`

| Member | Description |
| --- | --- |
| `records` | `list[ExcRecord]` |
| `handled` / `unhandled` | Records swallowed inside / escaped from the traced scope |
| `to_list()` | JSON-serialisable list of records |
| `export_json(path)` | Write the JSON document directly to `path` |
| `format_report(setcolor=False)` | Return the exception report as a string |
| `print_report(setcolor=False)` | Print the report to stdout |

## Removed APIs

`logging_path` and the interactive-shell parameters (`interactive`,
`interactive_on_event`, `interactive_filter`) are no longer part of the API.
See the [Migration Guide](migration.md).
