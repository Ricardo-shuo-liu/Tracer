# Trace.py
import functools
import sys
from typing import Callable, List
from .TraceContext import TraceContext
from .Parser import frame_callback

def tracer(
        trace_fn: List[Callable] | None = None,
        trace_entity=False) -> Callable:
    """A decorator that prints a function's name, args, and return values."""
    def include(fn: Callable) -> Callable:
        target_names = set()
        if trace_entity:
            target_names.add(fn.__name__)
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)
        target_names = target_names if target_names else None
        
        @functools.wraps(fn)
        def wrapped(*args, **kwds):
            ctx = TraceContext()
            def hook(frame, event, arg):
                return frame_callback(ctx, target_names, frame, event, arg)

            sys.settrace(hook)
            result = fn(*args, **kwds)
            sys.settrace(None)
            return result
        return wrapped
    return include
