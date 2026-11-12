# Migration Guide

This page describes the API changes introduced by the writer-based output
pipeline.

## `logging_path` → `output_way`

The `logging_path` parameter was removed from both the `tracer` decorator and
the `Tracer` context manager. Use `output_way` instead:

```python
# Before
@tracer(trace_entity=True, logging_path="trace.log")
def run():
    ...

# After
@tracer(trace_entity=True, output_way="trace.log")
def run():
    ...
```

### Console output changed

The old `logging_path` implementation wrote the trace to the file **and**
printed it to the console. `output_way="trace.log"` writes to the file only. To
keep both destinations, list them explicitly:

```python
@tracer(trace_entity=True, output_way=[None, "trace.log"])
def run():
    ...
```

`None` selects the console destination. The default console stream is now
`stderr`; previously trace lines were printed to `stdout`.

### File format changed

The old implementation used Python's `logging` module and prefixed each line
with a timestamp (`%(asctime)s | %(message)s`). File output is now the plain
trace text, identical to console output, without timestamps.

### Reports follow the output target

Timing and exception reports used to be printed to `stdout` regardless of
`logging_path`. They now go through the same `output_way` pipeline as the trace,
so a file destination receives the complete document.

## Interactive parameters removed

The following parameters were removed:

- `interactive`
- `interactive_on_event`
- `interactive_filter`

Use `breakpoint()`, `pdb.set_trace()` or your IDE debugger for interactive
inspection. The `tracer/interact` module and its tests were deleted.

## `overwrite`

`overwrite=True` truncates each file destination on its first write, then
appends for the rest of the writer's lifetime. It has no effect on callables and
streams. A mixed destination list is allowed; only file targets are truncated.

## Removed module

`tracer/core/Log.py` was removed. All output is handled by
`tracer/writer/WorkFlow.py` and `tracer/writer/Writer.py`.
