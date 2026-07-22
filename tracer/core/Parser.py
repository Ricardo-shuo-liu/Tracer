# Parser.py
from typing import Callable
from .TraceContext import TraceContext
from tracer.interact import SetInteract
def frame_callback(
        ctx: TraceContext,
        target_set: set | None,
        interactive_on_event:bool,
        frame,
        event,
        arg
) -> Callable | None:
    func_name = frame.f_code.co_name

    if target_set is not None and func_name not in target_set:
        return None
    
    output_line: str | None = None

    if event == "call":
        if ctx.time_trace and ctx.stats:
            ctx.stats.enter_func(frame, func_name)
        var_names = frame.f_code.co_varnames
        args_str = [f"{name}={repr(frame.f_locals[name])}" for name in var_names]
        arg_text = ", ".join(args_str)
        output_line = f"{ctx.prefix}-> {func_name}({arg_text})"
        if interactive_on_event:
            namespace = {}
            namespace.update(globals())
            namespace.update(frame.f_locals)
            SetInteract(namespace=namespace,func_name=func_name,event=event,arg_text=arg_text)
        ctx.indent()

    elif event == "return":
        cost = None
        if ctx.time_trace and ctx.stats:
            _,cost = ctx.stats.exit_func(frame)

        if cost is not None:
            output_line = f"{ctx.prefix}<- {func_name} returned {repr(arg)} | cost={cost:.6f}s"
        else:
            output_line = f"{ctx.prefix}<- {func_name} returned {repr(arg)}"

        if interactive_on_event:
            namespace = {}
            namespace.update(globals())
            namespace.update(frame.f_locals)
            SetInteract(namespace=namespace,func_name=func_name,event=event,returned=repr(arg))

        ctx.dedent()

    if output_line is not None:
        ctx.add(output_line)
    def next_hook(f, e, a):
        return frame_callback(ctx, target_set,interactive_on_event,f, e, a)
    return next_hook
