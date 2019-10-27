#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_role_permission.py
@create date: 2019-10-27 14:52 
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
from core.role_permission_singleton import role_permission_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg


class interfaceRolePermission(Resource):

    @api_version
    @login_required
    def get(self, version, role_id=None):
        xml = request.args.get('format')
        try:
            if role_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            data = role_permission_singleton.get_role_permission_info(role_id)
            body = modelEnum.role_permission.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def post(self, version, role_id=None):
        xml = request.args.get('format')
        try:
            if role_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.role_permission.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['per_keys']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'per_keys': list}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            per_keys = str(request_data.get('per_keys'))
            data = role_permission_singleton.add_role_permission(role_id, per_keys)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)
