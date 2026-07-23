# Trace.py
import functools
import sys
from typing import Callable, List
from .TraceContext import TraceContext
from .Parser import frame_callback
from .Log import Log
from tracer.interact import SetInteract

def tracer(
        trace_fn: List[Callable] | None = None,
        trace_entity:bool=False,
        logging_path:str | None = None,
        time_trace:bool=False,
        interactive:bool= False,
        interactive_on_event:bool=False,
        interactive_filter:List[Callable]|None = None,
        use_color:bool=False) -> Callable:
    """
    Decorator to capture function call stack, print hierarchical invocation tree,
    support execution time statistics and interactive debugging.

    Args:
        trace_fn: List of additional target functions to trace. Set None if no extra functions need tracking.
        trace_entity: If True, trace the decorated function itself.
        logging_path: File path for log persistence. If None, logs will only print to console without file output.
        time_trace: Enable runtime statistics. Records invocation count and execution time, and prints summary report after execution completes.
        interactive: If True, launch an interactive Python shell once before tracing starts at the top-level entry.
            Type exit() to resume program execution.
        interactive_on_event: If True, pause and open interactive shell on every call / return event of traced functions.
            WARNING: Reserved for deep debugging only.
            Blocking inside trace callback may lead to unstable tracing. Not recommended for regular use.

    Examples:
        >>> # Basic usage: trace the decorated function and print tree log to console
        >>> @tracer(trace_entity=True)
        >>> def fib(n):
        >>>     if n <= 1:
        >>>         return n
        >>>     return fib(n - 2) + fib(n - 1)

        >>> # Trace self and inner functions, save logs into file
        >>> @tracer(trace_fn=[add, chain], trace_entity=True, logging_path="./trace.log")
        >>> def run():
        >>>     return chain(3)

        >>> # Enable execution time statistics
        >>> @tracer(trace_entity=True, time_trace=True)
        >>> def fib(n):
        >>>     ...

        >>> # Enter interactive shell before tracing starts
        >>> @tracer(trace_entity=True, interactive=True)
        >>> def fib(n):
        >>>     ...

        >>> # Debug mode: pause on each function call / return (debug only)
        >>> @tracer(trace_entity=True, interactive_on_event=True)
        >>> def fib(n):
        >>>     ...
    """
    def include(fn: Callable) -> Callable:
        target_names = set()
        if trace_entity:
            target_names.add(fn.__name__)
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)
        target_names = target_names if target_names else None

        filter = set()

        if interactive_filter:
            filter.update(f.__name__ for f in interactive_filter)
        filter = filter if filter else None
        logger = Log(logging_path=logging_path).get_logger() if logging_path else None
       
        ctx = TraceContext(logger=logger,
                           time_trace=time_trace,
                           set_color=use_color)
        @functools.wraps(fn)
        def wrapped(*args, **kwds):
            def hook(frame, event, arg):
                return frame_callback(ctx,
                                      target_names,
                                      interactive_on_event,
                                      filter,
                                      frame,
                                      event,
                                      arg)
            
            depth = getattr(wrapped, "_depth", 0)

            if depth == 0:
                ctx.prefix = ""
                
                if interactive:
                    namespace = {}
                    f = ""
                    for arg in args:
                        f += f"{arg},"
                    for k, v in kwds.items():
                        f += f"{k}={v},"

                    namespace.update(globals())
                    namespace.update(locals())
                    SetInteract(namespace=namespace,
                                func_name=str(fn.__name__),
                                event="call",
                                arg_text=f"{f}"[:-1])
                    print(f"{f}"[:-1])
                sys.settrace(hook)    
            setattr(wrapped, "_depth", depth + 1)
            try:
                return fn(*args, **kwds)
            finally:
                new_depth = getattr(wrapped, "_depth") - 1
                setattr(wrapped, "_depth", new_depth)
                if new_depth == 0:
                    sys.settrace(None)
                    ctx.outputcontrol()
                    if ctx.time_trace and ctx.stats:
                        ctx.stats.print_report(setcolor=ctx.set_color)

        return wrapped
    return include

class Tracer:
    def __init__(self,
                 trace_fn: List[Callable] | None = None,
                 logging_path:str|None = None,
                 time_trace:bool=False,
                 interactive:bool= False,
                 interactive_on_event:bool=False,
                 interactive_filter:List[Callable]|None = None,
                 use_color:bool=False):
        """
        Context manager version of tracing utility, supports `with` syntax.
        Captures function call stack, prints hierarchical invocation tree,
        collects runtime statistics and provides interactive debugging.

        Args:
            trace_fn: List of additional target functions to trace. Set None if no extra functions need tracking.
            logging_path: File path for log persistence. If None, logs will only print to console without file output.
            time_trace: Enable runtime statistics. Records invocation count and execution time, and prints summary report after execution completes.
            interactive: If True, launch an interactive Python shell once before tracing starts.
                Type exit() to resume program execution.
            interactive_on_event: If True, pause and open interactive shell on every call / return event of traced functions.
                WARNING: Reserved for deep debugging only.
                Blocking inside trace callback may lead to unstable tracing. Not recommended for regular use.

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
            >>> with Tracer(trace_fn=[fib], logging_path="./trace.log"):
            >>>     res = fib(3)

            >>> # Enter interactive shell before tracing starts
            >>> with Tracer(trace_fn=[fib], interactive=True):
            >>>     res = fib(3)
        """
        target_names = set()
        self.interactive = interactive
        self.interactive_on_event = interactive_on_event
        if trace_fn is not None:
            target_names.update(f.__name__ for f in trace_fn)

        self.target_names = target_names if target_names else None

        filter = set()
        if interactive_filter:
            filter.update(f.__name__ for f in interactive_filter)
        self.filter = filter if filter else None

        logger = Log(logging_path=logging_path).get_logger() if logging_path else None
        self.ctx = TraceContext(logger=logger,time_trace=time_trace,set_color=use_color)
    def hook(self, frame, event, arg):
        return frame_callback(self.ctx,
                              self.target_names,
                              self.interactive_on_event,
                              self.filter,
                              frame, event, arg)
    def __enter__(self):
        if self.interactive:
            namespace = {}
            namespace.update(globals())
            namespace.update(locals())
            SetInteract(namespace=namespace,
                        func_name="",
                        event="call",
                        arg_text="++++++")
        sys.settrace(self.hook)
    def __exit__(self, *_):
        sys.settrace(None)
        self.ctx.outputcontrol()
        if self.ctx.time_trace and self.ctx.stats:
            self.ctx.stats.print_report(setcolor=self.ctx.set_color)