from . import PathLike,WritableStream,shitcode
from .FileWriter import FileWriter
import sys

class Writer():
    def __init__(self,output, overwrite):
        is_path = isinstance(output, (PathLike, str, bytes))
        self.write = None

        if overwrite and not is_path:
            raise ValueError(
                '`overwrite=True` can only be used when writing content to file.'
            )

        if output is None:
            def write(s):
                stderr = sys.stderr
                try:
                    stderr.write(s)
                except UnicodeEncodeError:
                    stderr.write(shitcode(s))
            self.write = write

        elif is_path:
            self.write = FileWriter(output, overwrite).write

        elif callable(output):
            self.write = output

        else:
            if not isinstance(output, WritableStream):
                raise TypeError(
                    'output_way must be None, a file path, a callable, or an '
                    'object with a write() method; got '
                    f'{type(output).__name__!r}'
                )
            def write(s):
                output.write(s)
            self.write = write
    def __call__(self,s):
        self.write(s)

    