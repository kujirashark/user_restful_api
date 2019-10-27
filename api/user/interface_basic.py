#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_basic.py
@create date: 2019-10-27 14:54 
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


class interfaceUserBasic(Resource):
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

                fields = ['user_name', 'login_name', 'phone', 'email']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)
                par_type = {'user_name': str, 'login_name': str, 'phone': str,'email':str}
                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)

                request_data['user_id'] = user_id
                data = user_singleton.update_header_user_info(request_data)
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)