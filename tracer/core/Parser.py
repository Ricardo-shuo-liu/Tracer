# Parser.py
from typing import Callable
from .TraceContext import TraceContext

def frame_callback(
        ctx: TraceContext,
        target_set: set | None,
        frame,
        event,
        arg
) -> Callable | None:
    func_name = frame.f_code.co_name

    if target_set is not None and func_name not in target_set:
        return None

    if event == "call":
        var_names = frame.f_code.co_varnames
        args_str = [f"{name}={repr(frame.f_locals[name])}" for name in var_names]
        arg_text = ", ".join(args_str)
        print(f"{ctx.prefix}-> {func_name}({arg_text})")
        ctx.indent()

    elif event == "return":
        print(f"{ctx.prefix}<- {func_name} returned {repr(arg)}")
        ctx.dedent()
        

    def next_hook(f, e, a):
        return frame_callback(ctx, target_set, f, e, a)
    return next_hook
