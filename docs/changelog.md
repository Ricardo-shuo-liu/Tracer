# Changelog

## Unreleased

### Added

- Writer-based output pipeline (`WorkFlow`, `Writer`, `FileWriter`) with
  `output_way` and `overwrite`.
- Support for console, file paths (`str`/`bytes`/`os.PathLike`), callables,
  writable streams and multiple destinations.
- Per-run reset of timing data and exception records.
- Safe `repr()` formatting in the trace hook.
- Restoration of the previously installed `sys.settrace` hook.
- mkdocs-material documentation with English and Chinese pages.

### Changed

- Default output is now `stderr`.
- Timing and exception reports are written through `output_way` instead of
  `stdout`.
- Color is enabled only when every destination is console-like; ANSI codes are
  never written to files.
- The exception JSON export is protected so a write failure cannot mask the
  original exception.
- `overwrite=True` applies to file destinations only and is allowed in mixed
  destination lists.

### Removed

- `logging_path` (use `output_way`).
- `interactive`, `interactive_on_event`, `interactive_filter`.
- `tracer/interact/` and its tests.
- `tracer/core/Log.py`.
