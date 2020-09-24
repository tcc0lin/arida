#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/09/24 11:11:38
@Author  :   Lateautumn4lin 
@Version :   1.0
@Contact :   Lateautumn4lin
@License :   (C)Copyright 2020
@Desc    :   None
'''
from typing import (
    Dict,
    List,
    NoReturn
)
from pathlib import PosixPath
import subprocess
from loguru import logger
import execjs


def get_app_info(parse_path: PosixPath, frida_js_path: PosixPath) -> Dict[str, List[str]]:
    with open(parse_path, encoding="utf-8") as f, open(frida_js_path, encoding="utf-8") as f1:
        ctx = execjs.compile(f.read())
        result = ctx.call(
            'parse', f1.read()
        )
        return result


def name_transform(name: str) -> str:
    split_idx = 0
    for idx, s in enumerate(name):
        if s.isupper():
            split_idx = idx
    return f"{(name[:split_idx]).lower()}_{(name[split_idx:]).lower()}"


def detect_frida_state() -> str:
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


def start_frida_server() -> NoReturn:
    logger.info("Begin Start Frida Server")
    shell = 'adb shell su -c "./data/local/tmp/frida-server &"'
    subprocess.Popen(
        shell,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
