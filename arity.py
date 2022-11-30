from inspect import signature
from typing import Callable


def arity(func: Callable):
    return len(signature(func).parameters)


def is_zero(func: Callable):
    return arity(func) == 0
