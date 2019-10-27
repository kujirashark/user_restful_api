#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_user.py
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
from common.common_response_process import response_result_process
from core.user_singleton import user_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg
from utils.status_code import response_code


class interfaceUser(Resource):
    @api_version
    @login_required
    def get(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            body = modelEnum.user.value.get('body')
            if user_id is None:
                request_data = req.request_process(request, xml, modelEnum.user.value)
                if isinstance(request_data, bool):
                    request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                    return response_result_process(request_data, xml=xml)
                if not request_data:
                    data = user_singleton.get_all_users()
                else:
                    fields = ['current_page', 'page_size']
                    must = req.verify_all_param_must(request_data, fields)
                    if must:
                        return response_result_process(must, xml=xml)
                    par_type = {'page_size': int, 'current_page': int, 'search_data': dict}
                    param_type = req.verify_all_param_type(request_data, par_type)
                    if param_type:
                        return response_result_process(param_type, xml=xml)

                    current_page, page_size = int(request_data.get('current_page')), int(request_data.get('page_size'))
                    search_data = request_data.get('search_data') if request_data.get('search_data') else {}
                    data = user_singleton.get_users_info(current_page, page_size, search_data)
            else:
                data = user_singleton.get_user_info_by_id(user_id)

            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def post(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            if user_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.user.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['user_name', 'login_name', 'user_sex', 'icon', 'position', 'email', 'phone', 'note_info', 'icon',
                      'role_ids', 'group_ids', 'dpt_ids']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'user_name': str, 'login_name': str, 'user_sex': int, 'icon': str, 'position': str,
                        'email': str, 'phone': str, 'note_info': str,
                        }
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)

            data = user_singleton.add_user(request_data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
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

                fields = ['user_name', 'login_name', 'user_sex', 'icon', 'position', 'email', 'phone', 'note_info',
                          'icon',
                          'role_ids', 'group_ids', 'dpt_ids']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)
                par_type = {'user_name': str, 'login_name': str, 'user_sex': int, 'icon': str, 'position': str,
                            'email': str, 'phone': str, 'note_info': str,
                            }
                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)
                request_data['user_id'] = user_id
                data = user_singleton.update_user(request_data)
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def delete(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            if user_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            if user_id is not None:
                data = user_singleton.delete_user([user_id])
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)
