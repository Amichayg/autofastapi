from fastapi import FastAPI
from pydantic import create_model
from inspect import signature, Signature, Parameter
import inspect
from typing import Callable
from types import ModuleType
from arity import is_zero
import example
from functools import partial


def signature_to_model(sig: Signature):
    def parse_parameter(param: Parameter):
        if param.default == inspect._empty:
            return param.annotation, ...
        return param.annotation, param.default

    return {
        param.name: parse_parameter(param)
        for param in sig.parameters.values()
    }


def func_as_pydantic_model(func: Callable):
    return create_model(f'{func.__name__} args', **signature_to_model(signature(func)))


def hello():
    return "whatsup"


def f(a: int):
    """ increments a by 1"""
    return a + 1


app = FastAPI()


def add_to_app(func: Callable):
    global app
    print('hey')
    if is_zero(func):
        app.get(f"/{func.__name__}")(func)
    else:
        model = func_as_pydantic_model(func)

        def inner(args: model):
            """panda"""
            return func(**args.dict())

        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        app.post(f'/{func.__name__}')(inner)


def add_module_to_app(module: ModuleType):
    def is_function(name: str) -> bool:
        return not name.startswith('__') and callable(getattr(module, name))

    functions = map(partial(getattr, module),
                    filter(is_function, dir(module)))

    list(map(add_to_app, functions))


add_to_app(f)
add_to_app(hello)
add_module_to_app(example)
if __name__ == '__main__':
    print(getattr(example, 'add'))