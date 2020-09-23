#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2020/09/22 18:52:11
@Author  :   Lateautumn4lin
@Version :   1.0
@Contact :   Lateautumn4lin
@License :   (C)Copyright 2020
@Desc    :   None
'''
from pydantic import BaseModel, Field, create_model
from typing import NewType
from ast import *
import types
from fastapi import APIRouter
import subprocess
import time
import frida
from frida import ServerNotRunningError
from fastapi import FastAPI
from loguru import logger
import execjs

app = FastAPI()
_parse_path = "parse.js"
_package_name = "com.kuaiduizuoye.scan"
_frida_js_path = f"apps/kuaiduizuoye.js"


def get_app_info():
    with open(_parse_path, encoding="utf-8") as f, open(_frida_js_path, encoding="utf-8") as f1:
        ctx = execjs.compile(f.read())
        result = ctx.call(
            'parse', f1.read()
        )
        return result


def on_message(message, data):
    if message['type'] == 'send':
        logger.info("[**] {0}".format(message['payload']))
    else:
        logger.info(f"log:{message}")


def detect_frida_state():
    logger.info("Begin Detect Frida State")
    shell = 'adb shell su -c "ps -ef|grep frida"'
    p = subprocess.Popen(
        shell,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    return ("frida-server" in stdout)


def start_frida_server():
    logger.info("Begin Start Frida Server")
    shell = 'adb shell su -c "./data/local/tmp/frida-server &"'
    subprocess.Popen(
        shell,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )


if not detect_frida_state():
    # 启动frida-server，增加延迟防止附加失败
    start_frida_server()
    time.sleep(3)
session = frida.get_usb_device().attach(_package_name)
script = session.create_script(
    open(_frida_js_path, encoding="utf-8").read()
)
script.on('message', on_message)
logger.info('[*] Start attach')
script.load()
Url = create_model("User", **{"origin_url": "asdasd"})
function_ast = FunctionDef(
    lineno=2,
    col_offset=0,
    name='generate_url',
    args=arguments(
        args=[
            arg(
                lineno=2,
                col_offset=17,
                arg='item',
                annotation=Name(lineno=2, col_offset=22,
                                id='Url', ctx=Load()),
            ),
        ],
        posonlyargs=[],
        vararg=None,
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=None,
        defaults=[],
    ),
    body=[
        Expr(
            lineno=3,
            col_offset=4,
            value=Call(
                lineno=3,
                col_offset=4,
                func=Name(lineno=3, col_offset=4,
                          id='print', ctx=Load()),
                args=[Name(lineno=3, col_offset=10,
                           id='Url', ctx=Load())],
                keywords=[],
            ),
        ),
        Assign(
            lineno=4,
            col_offset=4,
            targets=[Name(lineno=4, col_offset=4,
                          id='res', ctx=Store())],
            value=Call(
                lineno=4,
                col_offset=10,
                func=Attribute(
                    lineno=4,
                    col_offset=10,
                    value=Attribute(
                        lineno=4,
                        col_offset=10,
                        value=Name(lineno=4, col_offset=10,
                                   id='script', ctx=Load()),
                        attr='exports',
                        ctx=Load(),
                    ),
                    attr='generate_url',
                    ctx=Load(),
                ),
                args=[
                    Attribute(
                        lineno=4,
                        col_offset=38,
                        value=Name(lineno=4, col_offset=38,
                                   id='item', ctx=Load()),
                        attr='origin_url',
                        ctx=Load(),
                    ),
                ],
                keywords=[],
            ),
        ),
        Return(
            lineno=5,
            col_offset=4,
            value=Name(lineno=5, col_offset=11, id='res', ctx=Load()),
        ),
    ],
    decorator_list=[],
    returns=None,
)
module_ast = Module(body=[function_ast], type_ignores=[])
module_code = compile(module_ast, "<>", "exec")
function_code = [
    c for c in module_code.co_consts if isinstance(c, types.CodeType)][0]
test = types.FunctionType(
    function_code,
    {
        "script": script,
        "Url": Url,
        "print": print
    }
)
test.__annotations__ = {"item": Url}

router = APIRouter()
for k, v in get_app_info().items():
    router.add_api_route("/generate_url", test, methods=["POST"])
    break
app.include_router(router)


# @app.post('/generate_url')
# def generate_url(item: c):
#     res = script.exports.generate_url(item.origin_url)
#     return res
