#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: common_login_helper.py
@create date: 2019-10-27 14:49 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from functools import wraps
from os import abort
from flask import request, g

from utils.auth_helper import Auth


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_key = Auth.identify(request)
        if user_key > 0:
            g.user_key = user_key
            ###token验证，服务于restful
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


###权限验证装饰器
def login_super(func):
    @wraps(func)
    def wrapper():
        if g.user_key != 1:
            abort(403)
        return func()

    return wrapper
