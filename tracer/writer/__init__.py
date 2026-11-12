# 这个部分实现思路来自 Ram Rachum 的项目
# Link: https://github.com/cool-RR/PySnooper
# 如果存在侵权联系删除


from tracer.abc import ABC
import abc
import os
import sys

PY3 = (sys.version_info[0] == 3)
PY2 = not PY3
if PY3:
    string_types = (str,)
    text_type = str
    binary_type = bytes
else:
    string_types = (basestring,)
    text_type = unicode
    binary_type = str

def shitcode(s):
    return ''.join(
        (c if (0 < ord(c) < 256) else '?') for c in s
    )


def _check_methods(C, *methods):
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True


class WritableStream(ABC):
    @abc.abstractmethod
    def write(self, s):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is WritableStream:
            return _check_methods(C, 'write')
        return NotImplemented

if hasattr(os, 'PathLike'):
    PathLike = os.PathLike
else:
    class PathLike(ABC):
        """Abstract base class for implementing the file system path protocol."""

        @abc.abstractmethod
        def __fspath__(self):
            """Return the file system path representation of the object."""
            raise NotImplementedError

        @classmethod
        def __subclasshook__(cls, subclass):
            return (
                hasattr(subclass, '__fspath__') or
                # Make a concession for older `pathlib` versions:g
                (hasattr(subclass, 'open') and
                 'path' in subclass.__name__.lower())
            )


def normalize_output_way(output_way):
    """Normalize the public ``output_way`` argument into a tuple of targets.

    Single destinations are wrapped into a one-element tuple. Everything else
    is treated as a collection of destinations.

    ``str``/``bytes``/``PathLike`` and writable stream objects are themselves
    iterable (``str`` yields characters, ``StringIO`` yields lines), so they
    must be matched explicitly before the generic iterable branch. Otherwise a
    file path would be split into one writer per character and a stream would
    be consumed as if it were a list of targets.
    """
    if (output_way is None
            or isinstance(output_way, (PathLike, str, bytes))
            or callable(output_way)
            or isinstance(output_way, WritableStream)):
        return (output_way,)
    try:
        return tuple(output_way)
    except TypeError:
        # Not iterable either: let Writer report the unsupported type.
        return (output_way,)



