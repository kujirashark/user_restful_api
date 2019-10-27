#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: common_log.py
@create date: 2019-10-27 14:40 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""



from functools import wraps
from flask import request, g, jsonify

from db.logger.db_log_mgr import db_log
from utils.fun_name_to_enum import functionName
from utils.status_code import response_code


def operation_log(description=''):
    """
    操作日志记录
    :param description:
    :return:
    """
    def _log(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            response = fun()
            ip_address = request.remote_addr
            user_key = g.user_key
            if user_key==None:
                return jsonify(response_code.LOGIN_TIMEOUT.value)
            model = getattr(functionName, description).value
            if response.json.get('code') == 200:
                ip_address = request.remote_addr
                level = 0
                des = model + functionName.success.value
                user_key = g.user_key
                db_log.add_operation_log(user_key, ip_address, level, des)
            else:
                level = 1
                des = model + functionName.fail.value
                db_log.add_operation_log(user_key, ip_address, level, des)
            return response
        return wrapper
    return _log
