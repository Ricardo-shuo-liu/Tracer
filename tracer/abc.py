

import abc


if hasattr(abc, 'ABC'):
    ABC = abc.ABC
else:
    class ABC(object):
        """Helper class that provides a standard way to create an ABC using
        inheritance.
        """
        __metaclass__ = abc.ABCMeta
        __slots__ = ()