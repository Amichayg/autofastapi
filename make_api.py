from fastapi import FastAPI
from pydantic import create_model
from inspect import signature, Signature, Parameter
import inspect
from typing import Callable
from arity import is_zero


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
    return create_model(func.__name__, **signature_to_model(signature(func)))


def hello():
    return "whatsup"


def f(a: int):
    """ increments a by 1"""
    return a + 1


app = FastAPI()


def add_to_app(func: Callable):
    global app
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


add_to_app(f)
add_to_app(hello)