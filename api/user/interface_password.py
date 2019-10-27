#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_password.py
@create date: 2019-10-27 14:53 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from flask import request
from flask_restful import Resource

from common.common_login_helper import login_required
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_code import response_code
from common.common_response_process import response_result_process
from core.user_singleton import user_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg


class interfacePassword(Resource):

    @api_version
    @login_required
    def post(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            if user_id is  None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            data = user_singleton.reset_password([user_id])
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def put(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            if user_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            if user_id is not None:
                request_data = req.request_process(request, xml, modelEnum.user.value)
                if isinstance(request_data, bool):
                    request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                    return response_result_process(request_data, xml=xml)
                if not request_data:
                    data = response_code.REQUEST_PARAM_MISSED
                    return response_result_process(data, xml=xml)

                fields = ['old_password', 'new_password', 'new_password_ok']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)
                par_type = {'old_password': str, 'new_password': str,  'new_password_ok': str}
                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)

                old_pwd = request_data.get('old_password')
                new_pwd = request_data.get('new_password')
                new_pwd_ok = request_data.get('new_password_ok')

                # 判断输入的数据是否为空
                if not all([user_id, old_pwd, new_pwd_ok]):
                    error_data = response_code.PASS_WORD_INFO_NOT_FILL
                    return response_result_process(error_data, xml=xml)
                # 核对两次输入的密码是否一致
                if new_pwd_ok != new_pwd:
                    error_data = response_code.TWO_PASS_WORD_DIFFERENT
                    return response_result_process(error_data, xml=xml)

                data = user_singleton.update_user_password(user_id, old_pwd, new_pwd)
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)