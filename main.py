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
from fastapi.openapi.utils import get_openapi
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
_frida_js_path1 = Path(__file__).absolute().parent/"apps/yuxueyuan.js"
_frida_js_path = Path(__file__).absolute().parent/"apps/kuaiduizuoye.js"
_package_name = "com.kuaiduizuoye.scan"
_package_name1 = "com.drcuiyutao.babyhealth"

# frida启动前检测
if not detect_frida_state():
    # 启动frida-server，增加延迟防止附加失败
    start_frida_server()
    time.sleep(3)

for app_info in INJECTION_APPS:
    session = frida.get_usb_device().attach(app_info["package_name"])
    app_info["absolute_path"] = Path(__file__).absolute().parent / \
        f"apps/{app_info['path']}.js"
    script = session.create_script(
        open(
            app_info["absolute_path"],
            encoding="utf-8"
        ).read()
    )
    script.load()
    app_info["script"] = script


def init_app() -> Starlette:
    app = FastAPI()
    # 每个app创建特有路由
    for app_info in INJECTION_APPS:
        router = APIRouter()
        for api_name, params in get_app_info(parse_path=PRASE_PATH, frida_js_path=app_info["absolute_path"]).items():
            params_dict = dict(zip(params, function_params_hints[api_name])) if (
                api_name in function_params_hints) else dict.fromkeys(params, "bb")
            model_name = f"{api_name}Model"
            Model = create_model(model_name, **params_dict)
            new_api_name = name_transform(api_name)
            func = generate_function(
                new_api_name,
                app_info["script"],
                model_name,
                Model
            )
            router.add_api_route(f"/{new_api_name}", func, methods=["POST"])
        app.include_router(
            router,
            prefix=f"/{app_info['path']}",
            tags=[app_info["name"]]
        )

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Arida框架",
            version="0.0.1",
            description="基于FastAPI实现的Frida-RPC工具   https://github.com/lateautumn4lin/arida",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi
    return app


app = init_app()
