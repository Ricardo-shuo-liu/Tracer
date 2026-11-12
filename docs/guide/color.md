# Color

Enable ANSI color with `use_color=True`:

```python
@tracer(trace_entity=True, use_color=True)
def run():
    ...
```

Color is applied to core trace content only: function names, return values,
costs, report headers and exception status lines. The rest of the output is
unchanged.

## Color support detection

At import time Tracer checks whether color is available:

- On Unix, `sys.stderr.isatty()` must be true and `tput colors` must report at
  least 8 colors.
- On Windows 10 build 10586 or newer, the console mode is enabled for the
  standard error handle.

The result is exposed as `tracer.core.Color.COLOR_SUPPORT`. If the terminal does
not support color, `use_color=True` has no effect and no escape sequences are
emitted.

## Files never receive ANSI codes

Color is enabled only when **every** configured destination is console-like:

- `None` (the default console destination)
- `sys.stdout` or `sys.stderr`
- a stream whose `isatty()` returns `True`

If any destination is a file, a callable or a non-terminal stream, color is
disabled for the whole run. This is deliberate: trace text is colorized before
it is fanned out to all destinations, so enabling color for a mixed list would
write escape sequences into the file.

```python
# No color: the file would otherwise receive ANSI codes.
@tracer(trace_entity=True, use_color=True, output_way=["trace.log", sys.stderr])
def run():
    ...
```

To get color, use a console-only destination:

```python
@tracer(trace_entity=True, use_color=True, output_way=sys.stderr)
def run():
    ...
```
