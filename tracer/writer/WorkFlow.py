from . import PathLike, normalize_output_way
from .Writer import Writer

class WorkFlow():
    def __init__(self, output_way, overwrite):
        targets = normalize_output_way(output_way)
        has_file_target = any(
            isinstance(target, (PathLike, str, bytes)) for target in targets
        )
        if overwrite and not has_file_target:
            raise ValueError(
                '`overwrite=True` can only be used when writing content to file.'
            )
        self.callable_stack = []
        for target in targets:
            is_file_target = isinstance(target, (PathLike, str, bytes))
            callable_write = Writer(
                target, overwrite if is_file_target else False
            )
            self.callable_stack.append(callable_write)
    def forward(self,s):
        # run workflow; a failing target must not block the remaining ones
        errors = []
        for callable_write in self.callable_stack:
            try:
                callable_write(s)
            except Exception as exc:
                errors.append(exc)
        if errors:
            raise errors[0]
        