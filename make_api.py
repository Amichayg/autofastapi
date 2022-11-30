from fastapi import FastAPI
from pydantic import create_model
from inspect import signature, Signature, Parameter
import inspect
from typing import Callable
from types import ModuleType
from arity import is_zero
import examplesource
from functools import partial
from fn import F, _


def signature_to_model(sig: Signature):
    def parse_parameter(param: Parameter):
        if param.default == inspect._empty:
            return param.annotation, ...
        return param.annotation, param.default

    return {
        param.name: parse_parameter(param)
        for param in sig.parameters.values()
    }


def func_name(func):
    return func.__name__ + str(signature(func))


def func_as_pydantic_model(func: Callable):
    return create_model(f'{func_name(func)} args', **signature_to_model(signature(func)))


app = FastAPI()


def add_to_app(app: FastAPI, func: Callable):
    if is_zero(func):
        def inner():
            return func()

        inner.__name__ = func_name(func)
        inner.__doc__ = func.__doc__
        app.get(f"/{func.__name__}")(inner)

    else:
        model = func_as_pydantic_model(func)

        def inner(args: model):
            return func(**args.dict())

        inner.__name__ = func_name(func)
        inner.__doc__ = func.__doc__
        app.post(f'/{func.__name__}')(inner)


def add_module_to_app(app: FastAPI, module: ModuleType):
    print('hey')
    def is_function(name: str) -> bool:
        return not name.startswith('__') and callable(getattr(module, name))

    functions = map(partial(getattr, module),
                    filter(is_function, dir(module)))

    list(map(partial(add_to_app, app), functions))


from importlib import import_module
from pathlib import Path

add_path = F(add_module_to_app, app) << import_module << F(_.stem)
list(map(add_path, Path('.').glob('*source.py')))