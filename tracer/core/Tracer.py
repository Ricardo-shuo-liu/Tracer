# Trace.py
import functools
import sys
from typing import Callable, List
from .TraceContext import TraceContext
from .Parser import frame_callback
from ..writer import normalize_output_way
from ..writer.WorkFlow import WorkFlow


def _is_console_target(target) -> bool:
    """Whether ANSI codes can safely be written to this target."""
    if target is None:
        return True
    if target is sys.stdout or target is sys.stderr:
        return True
    isatty = getattr(target, "isatty", None)
    if callable(isatty):
        try:
            return bool(isatty())
        except Exception:
            return False
    return False


def _color_enabled(use_color: bool, outputway) -> bool:
    """Color only when every target is a console-like stream, so ANSI codes
    never leak into files or non-terminal buffers."""
    return bool(use_color) and bool(outputway) and all(
        _is_console_target(t) for t in outputway
    )


def tracer(
        trace_fn: List[Callable] | None = None,
        trace_entity:bool=False,
        output_way = None,
        overwrite:bool = False,

        time_trace:bool=False,

        use_color:bool=False,

        exception_trace:bool=False,
        show_locals:bool=False,
        exception_json_path:str|None=None) -> Callable:
    """
    Decorator to capture function call stack, print hierarchical invocation tree,
    support execution time statistics and exception extraction.

    Args:
        trace_fn: List of additional target functions to trace. Set None if no extra functions need tracking.
        trace_entity: If True, trace the decorated function itself.
        output_way: Output destination. Accepts None (console, default), a file path
            (str/bytes/os.PathLike), a callable, an object with a write() method, or an
            iterable of these to write to multiple destinations.
        overwrite: Applies to file destinations only (ignored for streams/callables).
            If True, truncate each file on the first write instead of appending.
        time_trace: Enable runtime statistics. Records invocation count and execution time, and prints summary report after execution completes.
        exception_trace: If True, capture every exception raised inside the traced scope, including
            full traceback stack (even frames that are not traced), propagation path across traced
            functions, and whether it was swallowed or escaped. Prints a report after execution.
        show_locals: Only effective when exception_trace=True. Snapshot local variables at the frame
            where the exception was first observed.
        exception_json_path: Only effective when exception_trace=True. Dump the exception records to
            this JSON path after execution. Skipped if None.

    Examples:
        >>> # Basic usage: trace the decorated function and print tree log to console
        >>> @tracer(trace_entity=True)
        >>> def fib(n):
        >>>     if n <= 1:
        >>>         return n
        >>>     return fib(n - 2) + fib(n - 1)

        >>> # Trace self and inner functions, save logs into file
        >>> @tracer(trace_fn=[add, chain], trace_entity=True, output_way="./trace.log")
        >>> def run():
        >>>     return chain(3)

        >>> # Enable execution time statistics
        >>> @tracer(trace_entity=True, time_trace=True)
        >>> def fib(n):
        >>>     ...
    """
    def include(fn: Callable) -> Callable:

        outputway = normalize_output_way(output_way)
        workflow = WorkFlow(output_way=outputway,overwrite=overwrite)
        
        target_names = set()
        if trace_entity:
            target_names.add(fn.__name__)
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)
        target_names = target_names if target_names else None

        set_color = _color_enabled(use_color, outputway)
    
        ctx = TraceContext(workflow=workflow,
                           time_trace=time_trace,
                           set_color=set_color,
                           exception_trace=exception_trace,
                           show_locals=show_locals,
                           exception_json_path=exception_json_path)
        @functools.wraps(fn)
        def wrapped(*args, **kwds):
            def hook(frame, event, arg):
                return frame_callback(ctx, target_names, frame, event, arg)
            
            depth = getattr(wrapped, "_depth", 0)
            previous_trace = None

            if depth == 0:
                ctx.begin_run()
                previous_trace = sys.gettrace()
                sys.settrace(hook)
            setattr(wrapped, "_depth", depth + 1)
            try:
                return fn(*args, **kwds)
            finally:
                new_depth = getattr(wrapped, "_depth") - 1
                setattr(wrapped, "_depth", new_depth)
                if new_depth == 0:
                    # Restore whatever trace hook existed before us instead of
                    # clobbering an enclosing tracer / debugger / profiler.
                    sys.settrace(previous_trace)
                    ctx.finish()

        # expose the live context so callers can inspect records programmatically
        wrapped.tracer_ctx = ctx
        return wrapped
    return include

class Tracer:
    def __init__(self,
                 trace_fn: List[Callable] | None = None,
                 output_way = None,
                 overwrite:bool = False,

                 time_trace:bool=False,
                 use_color:bool=False,
                 exception_trace:bool=False,
                 show_locals:bool=False,
                 exception_json_path:str|None=None):
        """
        Context manager version of tracing utility, supports `with` syntax.
        Captures function call stack, prints hierarchical invocation tree,
        collects runtime statistics and extracts exceptions.

        Args:
            trace_fn: List of additional target functions to trace. Set None if no extra functions need tracking.
            output_way: Output destination. Accepts None (console, default), a file path
                (str/bytes/os.PathLike), a callable, an object with a write() method, or an
                iterable of these to write to multiple destinations.
            overwrite: Applies to file destinations only (ignored for streams/callables).
                If True, truncate each file on the first write instead of appending.
            time_trace: Enable runtime statistics. Records invocation count and execution time, and prints summary report after execution completes.
            exception_trace: If True, capture every exception raised inside the traced scope, including
                full traceback stack (even frames that are not traced), propagation path across traced
                functions, and whether it was swallowed or escaped. Prints a report on exit.
            show_locals: Only effective when exception_trace=True. Snapshot local variables at the frame
                where the exception was first observed.
            exception_json_path: Only effective when exception_trace=True. Dump the exception records to
                this JSON path on exit. Skipped if None.

        Examples:
            >>> def fib(n):
            >>>     if n <= 1:
            >>>         return n
            >>>     return fib(n - 2) + fib(n - 1)

            >>> # Basic usage: trace fib and print call tree
            >>> with Tracer(trace_fn=[fib]):
            >>>     res = fib(3)

            >>> # Enable time statistics and output summary report
            >>> with Tracer(trace_fn=[fib], time_trace=True):
            >>>     res = fib(3)

            >>> # Persist logs to file
            >>> with Tracer(trace_fn=[fib], output_way="./trace.log"):
            >>>     res = fib(3)
        """
        outputway = normalize_output_way(output_way)
        workflow = WorkFlow(output_way=outputway,overwrite=overwrite)

        target_names = set()
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)

        self.target_names = target_names if target_names else None

        set_color = _color_enabled(use_color, outputway)

        self.ctx = TraceContext(workflow=workflow,
                                time_trace=time_trace,
                                set_color=set_color,
                                exception_trace=exception_trace,
                                show_locals=show_locals,
                                exception_json_path=exception_json_path)
        self._previous_trace = None
    @property
    def errors(self):
        """TraceErrors collector (None when exception_trace is disabled)."""
        return self.ctx.errors
    @property
    def stats(self):
        return self.ctx.stats
    def hook(self, frame, event, arg):
        return frame_callback(self.ctx, self.target_names, frame, event, arg)
    def __enter__(self):
        self._previous_trace = sys.gettrace()
        self.ctx.begin_run()
        sys.settrace(self.hook)
        return self
    def __exit__(self, *_):
        sys.settrace(self._previous_trace)
        # returns None -> exceptions raised in the block keep propagating
        self.ctx.finish()