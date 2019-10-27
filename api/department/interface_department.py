#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_department.py
@create date: 2019-10-27 14:48 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from flask import request
from flask_restful import Resource

from common.common_login_helper import login_required
from common.common_request_process import req
from common.common_response_process import response_result_process
from core.department_singleton import department_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg
from utils.status_code import response_code
from common.common_model_enum import modelEnum


class interfaceDepartment(Resource):
    @api_version
    @login_required
    def get(self, version,dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            data = department_singleton.get_department()
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def post(self,version,dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['dpt_name', 'p_id']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'dpt_name': str, 'p_id': int}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            dpt_name,dpt_p_id = request_data.get('dpt_name'),request_data.get('p_id')
            data = department_singleton.add_department(dpt_name, dpt_p_id)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def put(self,version,dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is None:
                data = response_code.NOT_FOUND
                return  response_result_process(data, xml=xml)

            if dpt_id is not None:
                request_data = req.request_process(request, xml, modelEnum.department.value)
                if isinstance(request_data, bool):
                    request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                    return response_result_process(request_data, xml=xml)
                if not request_data:
                    data = response_code.REQUEST_PARAM_MISSED
                    return response_result_process(data, xml=xml)

                fields = ['dpt_name','p_id']
                must = req.verify_all_param_must(request_data, fields)
                if must:
                    return response_result_process(must, xml=xml)

                par_type =  {'dpt_name': str, 'p_id': int}

                param_type = req.verify_all_param_type(request_data, par_type)
                if param_type:
                    return response_result_process(param_type, xml=xml)
                dpt_name = request_data.get('dpt_name')
                p_id = request_data.get('p_id')
                data = department_singleton.update_department(dpt_id, dpt_name,p_id)
                return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.UPDATE_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def delete(self,version,dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            if dpt_id is not None:
                data = department_singleton.delete_department(dpt_id)
                return response_result_process(data, xml=xml)

        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)