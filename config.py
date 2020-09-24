#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2020/09/22 18:57:19
@Author  :   Lateautumn4lin 
@Version :   1.0
@Contact :   Lateautumn4lin
@License :   (C)Copyright 2020
@Desc    :   None
'''
from pathlib import Path
PRASE_PATH = Path(__file__).absolute().parent / "parse.js"
INJECTION_APPS = [
    {
        "name": "育学园",
        "path": "yuxueyuan",
        "package_name": "com.drcuiyutao.babyhealth"
    },
    {
        "name": "快读作业",
        "path": "kuaiduizuoye",
        "package_name": "com.kuaiduizuoye.scan"
    }
]
