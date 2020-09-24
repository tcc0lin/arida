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
from pathlib import Path
from pydantic import BaseModel, Field, create_model
from fastapi import APIRouter
import time
import frida
from starlette.applications import Starlette
from fastapi import FastAPI
from loguru import logger
from utils.generate_function import generate_function
from utils import (
    name_transform,
    detect_frida_state,
    start_frida_server,
    get_app_info
)
from config import *

# 配置相关函数的参数类型列表
function_params_hints = {
    "encryptData": [0, 0, 0, 0, "", 0, 0, 0, 0, 0, 0]
}
# app相关信息
_frida_js_path = Path(__file__).absolute().parent/"apps/kuaiduizuoye.js"
_package_name = "com.kuaiduizuoye.scan"

# frida注入
if not detect_frida_state():
    # 启动frida-server，增加延迟防止附加失败
    start_frida_server()
    time.sleep(3)
session = frida.get_usb_device().attach(_package_name)
script = session.create_script(
    open(_frida_js_path, encoding="utf-8").read()
)
script.load()


def init_app() -> Starlette:
    app = FastAPI()
    # 每个app创建特有路由
    router = APIRouter()
    for api_name, params in get_app_info(parse_path=PRASE_PATH, frida_js_path=_frida_js_path).items():
        params_dict = dict(zip(params, function_params_hints[api_name])) if (
            api_name in function_params_hints) else dict.fromkeys(params, "bb")
        model_name = f"{api_name}Model"
        Model = create_model(model_name, **params_dict)
        new_api_name = name_transform(api_name)
        func = generate_function(
            new_api_name,
            script,
            model_name,
            Model
        )
        router.add_api_route(f"/{new_api_name}", func, methods=["POST"])
    # 全局添加各app路由类
    app.include_router(router)
    return app


app = init_app()
