# Trace.py
import functools
import sys
from typing import Callable, List
from .TraceContext import TraceContext
from .Parser import frame_callback
from .Log import Log
def tracer(
        trace_fn: List[Callable] | None = None,
        trace_entity:bool=False,
        logging_path:str | None = None,
        time_trace:bool=False) -> Callable:
    """A decorator that prints a function's name, args, and return values."""
    def include(fn: Callable) -> Callable:
        target_names = set()
        if trace_entity:
            target_names.add(fn.__name__)
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)
        target_names = target_names if target_names else None
        
        logger = Log(logging_path=logging_path).get_logger() if logging_path else None
        ctx = TraceContext(logger=logger,time_trace=time_trace)
        @functools.wraps(fn)
        def wrapped(*args, **kwds):
            def hook(frame, event, arg):
                return frame_callback(ctx, target_names, frame, event, arg)
            
            depth = getattr(wrapped, "_depth", 0)

            if depth == 0:
                ctx.prefix = ""
                sys.settrace(hook)
            
            setattr(wrapped, "_depth", depth + 1)
            try:
                return fn(*args, **kwds)
            finally:
                new_depth = getattr(wrapped, "_depth") - 1
                setattr(wrapped, "_depth", new_depth)
                if new_depth == 0:
                    sys.settrace(None)
                    if ctx.time_trace and ctx.stats:
                        ctx.stats.print_report()
        return wrapped
    return include

class Tracer:
    def __init__(self,
                 trace_fn: List[Callable] | None = None,
                 logging_path:str|None = None,
                 time_trace:bool=False):
        target_names = set()
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)
        self.target_names = target_names if target_names else None
        logger = Log(logging_path=logging_path).get_logger() if logging_path else None
        self.ctx = TraceContext(logger=logger,time_trace=time_trace)
    def hook(self, frame, event, arg):
        return frame_callback(self.ctx, self.target_names, frame, event, arg)
    def __enter__(self):
        sys.settrace(self.hook)
    def __exit__(self, *_):
        sys.settrace(None)
        if self.ctx.time_trace and self.ctx.stats:
            self.ctx.stats.print_report()