# Limitations

## Tracing scope

### Async functions and generators are not traced

The hook is installed only around the call that creates the coroutine or
generator. Their bodies execute later, when awaited or iterated, after the hook
has been removed. Decorating an `async def` or a generator function therefore
produces no trace output.

The `Tracer` context manager can still trace code executed inside the `with`
block, including explicit `await` / iteration performed there.

### Functions are matched by name

`trace_fn` and `trace_entity` collect `__name__` values, not function objects.
Two functions with the same name in different modules are indistinguishable to
the tracer.

### An empty trace set traces everything

If the decorator receives neither `trace_entity=True` nor a `trace_fn`, or the
context manager receives `trace_fn=None`, the trace set is `None` and every frame
executed while the hook is active is traced. This includes standard-library and
third-party frames.

### Current thread only

`sys.settrace` is thread-local. Work performed in other threads is not traced.

## Output

### Buffered until the run ends

Trace lines are buffered and flushed once at the end of the top-level run.
Tracer is not a streaming logger: no output appears while the traced function is
still executing.

### Errors are reported, not raised

A failing destination is isolated and reported on `stderr`. An invalid path or a
broken callable does not fail at decoration time and does not abort the traced
function; it surfaces as a warning after the run. Use a destination whose
validity you control if you need fail-fast behavior.

### Relative paths resolve at flush time

File destinations are opened when output is flushed, not when the decorator is
created. A `chdir()` performed between decoration and flush changes where a
relative path is written.

### JSON export is separate

`exception_json_path` writes directly to the filesystem and is not part of
`output_way`. Its failures are reported as warnings.

## Color

Color capability is detected once at import time from `sys.stderr`. If streams
are redirected after import, the cached `COLOR_SUPPORT` value is not re-evaluated.
Color is disabled entirely for mixed destinations that include a file or a
non-terminal stream.

## Runtime cost

Tracer uses `sys.settrace` and formats every call and return event. It is a
diagnostic tool, not a sampling profiler; do not enable it on hot paths in
production.

## Interactive debugging

Interactive shell parameters were removed. Use Python's standard debugger
instead:

```python
breakpoint()          # or pdb.set_trace()
```

## Python version

Python 3.10.9 or newer is required.
