from fastapi import FastAPI
from pydantic import create_model
from inspect import signature, Signature, Parameter
import inspect
from typing import Callable


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


def f(a: int):
    return a + 1


app = FastAPI()
app.get("/")(lambda: "hello fastapi")


@app.post("/f")
async def do_f(args: func_as_pydantic_model(f)):
    return f(**args.dict())
