#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_role.py
@create date: 2019-10-27 14:51 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from flask import request
from flask_restful import Resource

from common.common_login_helper import login_required
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process
from core.role_permission_singleton import role_permission_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg
from utils.status_code import response_code


class interfaceRole(Resource):
    @api_version
    @login_required
    def get(self, version, role_id=None):
        xml = request.args.get('format')
        try:
            if role_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            request_data = req.request_process(request, xml, modelEnum.role.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = role_permission_singleton.get_all_roles()
            else:
                fields = ['current_page', 'page_size']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)
                par_type = {'page_size': int, 'current_page': int,'search_data':dict}
                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)

                current_page, page_size = int(request_data.get('current_page')), int(request_data.get('page_size'))
                search_data = request_data.get('search_data') if request_data.get('search_data') else {}

                data = role_permission_singleton.get_pages_roles(current_page,page_size,search_data)

            body = modelEnum.role.value.get('body')
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
            if role_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.role.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['role_name']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'role_name': str, 'note_info': str}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            role_name = request_data.get('role_name')
            note_info = request_data.get('note_info') if request_data.get('note_info') is not None else ''

            data = role_permission_singleton.add_role(role_name, note_info)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def put(self, version, role_id=None):
        xml = request.args.get('format')
        try:
            if role_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            if role_id is not None:
                request_data = req.request_process(request, xml, modelEnum.role.value)
                if isinstance(request_data, bool):
                    request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                    return response_result_process(request_data, xml=xml)
                if not request_data:
                    data = response_code.REQUEST_PARAM_MISSED
                    return response_result_process(data, xml=xml)

                fields = ['role_name']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)

                par_type = {'role_name': str, 'note_info':str}

                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)
                role_name = request_data.get('role_name')
                note_info = request_data.get('note_info') if request_data.get('note_info') else ''


                data = role_permission_singleton.update_role(role_id, role_name, note_info)
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def delete(self, version, role_id=None):
        xml = request.args.get('format')
        try:
            if role_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            if role_id is not None:
                data = role_permission_singleton.delete_role(role_id)
                return response_result_process(data, xml=xml)

        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)