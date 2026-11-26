#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: __init__.py.py
@create date: 2019-10-27 13:26 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from flask import Flask
from flask_cors import CORS


from api.resource import api
from utils.log_helper import init_log

from config import config, Config


def create_app(config_name):
    app = Flask(__name__)
    # 验证
    CORS(app,supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    ###初始化数据库
    # db.init_app(app)
    # 返回数据中response为中文（Flask>=2.3 需通过 json provider 设置，JSON_AS_ASCII 已失效）
    app.config['JSON_AS_ASCII'] = False
    if hasattr(app, 'json'):
        app.json.ensure_ascii = False


    ###初始化日志###
    init_log()
    api.init_app(app)
    return app