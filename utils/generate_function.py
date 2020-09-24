#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   generate_function.py
@Time    :   2020/09/24 10:23:37
@Author  :   Lateautumn4lin 
@Version :   1.0
@Contact :   Lateautumn4lin
@License :   (C)Copyright 2020
@Desc    :   None
'''
import types
from ast import *
from typing import Callable
from pydantic import BaseModel
from frida.core import Script


def generate_function(
    func_name: str,
    script: Script,
    model_name: str,
    model: BaseModel
) -> Callable:
    function_ast = FunctionDef(
        lineno=2,
        col_offset=0,
        name=func_name,
        args=arguments(
            args=[
                arg(
                    lineno=2,
                    col_offset=17,
                    arg='item',
                    annotation=Name(lineno=2, col_offset=23,
                                    id=model_name, ctx=Load()),
                ),
            ],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
            posonlyargs=[]
        ),
        body=[
            # Expr(
            #     lineno=3,
            #     col_offset=4,
            #     value=Call(
            #         lineno=3,
            #         col_offset=4,
            #         func=Name(lineno=3, col_offset=4,
            #                   id='print', ctx=Load()),
            #         args=[
            #             Call(
            #                 lineno=3,
            #                 col_offset=10,
            #                 func=Name(lineno=3, col_offset=10,
            #                           id='dict', ctx=Load()),
            #                 args=[Name(lineno=3, col_offset=15,
            #                            id='item', ctx=Load())],
            #                 keywords=[],
            #             ),
            #         ],
            #         keywords=[],
            #     ),
            # ),
            Assign(
                lineno=3,
                col_offset=4,
                targets=[Name(lineno=3, col_offset=4,
                              id='res', ctx=Store())],
                value=Call(
                    lineno=3,
                    col_offset=10,
                    func=Attribute(
                        lineno=3,
                        col_offset=10,
                        value=Attribute(
                            lineno=3,
                            col_offset=10,
                            value=Name(lineno=3, col_offset=10,
                                       id='script', ctx=Load()),
                            attr='exports',
                            ctx=Load(),
                        ),
                        attr=func_name,
                        ctx=Load(),
                    ),
                    args=[
                        Starred(
                            lineno=4,
                            col_offset=38,
                            value=Call(
                                lineno=4,
                                col_offset=39,
                                func=Attribute(
                                    lineno=4,
                                    col_offset=39,
                                    value=Call(
                                        lineno=4,
                                        col_offset=39,
                                        func=Name(
                                            lineno=4, col_offset=39, id='dict', ctx=Load()),
                                        args=[
                                            Name(lineno=4, col_offset=44, id='item', ctx=Load())],
                                        keywords=[],
                                    ),
                                    attr='values',
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[],
                            ),
                            ctx=Load(),
                        ),
                    ],
                    keywords=[],
                ),
            ),
            Return(
                lineno=4,
                col_offset=4,
                value=Name(lineno=4, col_offset=11, id='res', ctx=Load()),
            ),
        ],
        decorator_list=[],
        returns=None,
    )
    module_ast = Module(body=[function_ast], type_ignores=[])
    module_code = compile(module_ast, "<>", "exec")
    function_code = [
        c for c in module_code.co_consts if isinstance(c, types.CodeType)][0]
    function = types.FunctionType(
        function_code,
        {
            "script": script,
            model_name: model,
            "print": print,
            "dict": dict
        }
    )
    function.__annotations__ = {"item": model}
    return function
