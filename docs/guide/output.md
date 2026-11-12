# Output Redirection

Every trace line and every report is written through the same pipeline:

```text
TraceContext ──► WorkFlow ──► Writer ──► destination
                               ├─ console (stderr)
                               ├─ FileWriter
                               ├─ callable
                               └─ writable stream
```

`output_way` is normalized once when the decorator or context manager is
created. A single destination and a collection of destinations are both
accepted.

## Default output

`output_way=None` writes to the console. "Console" means `sys.stderr`, not
`sys.stdout`, so trace output can be redirected independently of normal program
output:

```python
@tracer(trace_entity=True)
def run():
    ...
```

```bash
python app.py 2> trace.log
```

## Supported destinations

| `output_way` value | Behavior |
| --- | --- |
| `None` | Write to `sys.stderr` |
| `str`, `bytes`, `os.PathLike` | Write UTF-8 text to the file |
| callable | Call `target(text)` with each output chunk |
| object with `write()` | Call `target.write(text)` |
| iterable of the above | Fan out each chunk to every destination |

Strings, bytes and `pathlib.Path` values are treated as **one** destination, not
as collections of characters. The same applies to streams.

### File path

```python
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

### Callable

```python
lines = []

@tracer(trace_entity=True, output_way=lines.append)
def run():
    ...
```

### Writable stream

```python
import io

buffer = io.StringIO()

@tracer(trace_entity=True, output_way=buffer)
def run():
    ...

print(buffer.getvalue())
```

### Multiple destinations

```python
@tracer(
    trace_entity=True,
    output_way=["trace.log", lines.append],
)
def run():
    ...
```

## Overwrite semantics

`overwrite` applies to **file destinations only**. It is ignored for callables
and streams.

- `overwrite=False` (default): append to existing files.
- `overwrite=True`: truncate each file on the first write, then append for the
  rest of the writer's lifetime.

```python
@tracer(trace_entity=True, output_way="trace.log", overwrite=True)
def run():
    ...
```

A mixed destination list such as `["trace.log", callback]` is allowed with
`overwrite=True`: the file is truncated, the callback is unaffected. If
`overwrite=True` is used with no file destination at all, `ValueError` is
raised when the decorator or context manager is created.

## Buffering

Trace lines are buffered until the top-level traced call finishes, then flushed
as one chunk. The timing and exception reports are emitted after that chunk.
Consequently, a file is opened at flush time rather than at decoration time.

## Failure handling

Destinations are isolated from each other:

- If one destination raises, the remaining destinations still receive the
  output.
- The output layer reports the failure to `stderr` and never replaces an
  exception escaping the traced scope.

This means an unwritable log file cannot turn a successful call into an error,
but it also means path errors surface as a warning after the run instead of
failing at decoration time.

## Color safety

Color is enabled only when every destination is a console-like stream. ANSI
escape sequences are therefore never written to files or non-terminal buffers.
See [Color](color.md).

## JSON export

`exception_json_path` is a separate artifact and does not go through
`output_way`. It writes a JSON document after the exception report. See
[Exception Tracing](exception-tracing.md).
