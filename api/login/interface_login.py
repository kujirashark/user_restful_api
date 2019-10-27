#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_login.py
@create date: 2019-10-27 14:36 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from flask import request, g
from flask_restful import Resource

from common.common_log import operation_log
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process

from utils.api_version_verify import api_version
from utils.auth_helper import Auth
from utils.log_helper import lg
from utils.status_code import response_code


class interfaceLogin(Resource):

    @api_version
    def post(self, version):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.login.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['login_name', 'login_password']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)

            login_name, login_password = request_data.get('login_name'), request_data.get('login_password')
            # 对登录情况进行验证
            dict_user = Auth.authenticate(login_name, login_password)
            # 将用户信息写到全局
            user_key = dict_user.get('id')
            operation_log(description='login')
            if user_key:
                g.user_key = user_key
                data = {}
                data['code'] = 200
                data['msg'] = '请求成功'
                data['data'] = dict_user
            else:
                data = dict_user

            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.LOGIN_FAIL
            return response_result_process(error_data, xml=xml)
