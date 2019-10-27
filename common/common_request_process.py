#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: common_request_process.py
@create date: 2019-10-27 14:08 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：请求处理
"""

import json
from json import JSONDecodeError

from common.common_api_version import apiVersion
from common.common_response_code import response_code
from common.common_response_log import ResponseLog
from common.common_response_process import response_result_process
from utils.log_helper import lg
from utils.xml_json_process import xml_to_json, is_none


class requestProcess(object):
    """
    请求处理
    """

    def _xml_request(self, request, model_json=None):
        """
        处理xml请求参数为json格式
        :param data: 请求
        :return:
        """
        try:
            data = request.data
            temp = data.decode('utf-8')
            if temp == '':
                return {}
            try:
                param_temp = xml_to_json(temp)
            except Exception as e:
                return response_code.REQUEST_PARAM_FORMAT_ERROR
            param = json.loads(param_temp)

            root = model_json.get('root')
            body = model_json.get('body')

            root_data = param.get(root)
            request_param = None
            if root_data:
                body_data = root_data.get(body)
                if body_data:
                    if isinstance(body_data,list):
                        request_param = is_none(root_data)
                    else:
                        request_param = is_none(body_data)
            if root_data is None:
                s_body_data = param.get(body)
                if s_body_data:
                    if isinstance(is_none(s_body_data), dict):
                        request_param = s_body_data

            if isinstance(request_param, list) or request_param is None:
                return False
            return request_param
        except Exception as e:
            lg.error(e)
            return False

    def _json_request(self, request):
        """
        处理json请求参数问题
        :param request: 请求
        :return:
        """
        try:
            request_data = request.data
            req_str = request_data.decode()
            if req_str == '':
                return {}
            data = json.loads(req_str)
            if isinstance(data, list):
                return False
            return data
        except JSONDecodeError as e:
            lg.error(e)
            return False

    def verify_one_param_type(self, param_name, value, type=None):
        """
        验证某个参数的类型
        :param param_name: 验证的参数名称
        :param value: 验证的参数的值
        :param type: 验证的参数的类型
        :return:
        """
        try:
            if type == float:
                v = None
                if isinstance(value,str):
                    v = eval(value)
                if isinstance(value,int):
                    v = value
                if isinstance(value,float):
                    v = value
                if isinstance(v, float):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == int:
                v = None
                if isinstance(value, str):
                    v = eval(value)
                if isinstance(value, float):
                    v = value
                if isinstance(value, int):
                    v = value
                if isinstance(v, int):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == str:
                if isinstance(value, str):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code

            if type == list:
                if isinstance(value, list):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
            if type == dict:
                if isinstance(value, dict):
                    pass
                else:
                    code = response_code.BAD_REQUEST
                    code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
                    return code
        except Exception as e:
            lg.error(e)
            code = response_code.BAD_REQUEST
            code['msg'] = ResponseLog.wrong_param_type(param_name, type.__name__)
            return code

    def verify_one_param_must(self, request_data: dict, param):
        """
        验证某个参数是否必填
        :param data: 请求的数据
        :param param: 本验证的字段
        :return:
        """
        if request_data.get(param) is None:
            code = response_code.BAD_REQUEST
            code['msg'] = ResponseLog.wrong_param_must(param)
            return code
        else:
            pass

    def verify_param_page(self, data, param):
        """
        验证是否有分页信息
        :param data:  验证的请求数据
        :param param: 是否有page字段
        :return:
        """
        page_data = data.get(param)
        if page_data.get('page_size') is not None:
            if page_data.get('current_page') is None:
                code = response_code.BAD_REQUEST
                code['msg'] = ResponseLog.wrong_param_must('current_page')
                return code
        if page_data.get('current_page') is not None:
            if page_data.get('page_size') is None:
                code = response_code.BAD_REQUEST
                code['msg'] = ResponseLog.wrong_param_must('page_size')
                return code

    def request_process(self, request, xml=None, model_json=None):
        """
        请求参数获取
        :param request: 请求
        :param xml:  请求响应类型 是否是xml 默认是json
        :return:
        """
        if xml is None:
            return self._json_request(request)
        if xml == 'xml':
            return self._xml_request(request, model_json)

    def verify_all_param_must(self, request_data: dict, fields: list):
        """
        批量验证是否是必传参数
        :param request_data: 请求的参数数据
        :param fields: ['a','b']
        :return:
        """
        for i in fields:
            must = self.verify_one_param_must(request_data, i)
            if must:
                return must
            else:
                pass

    def verify_all_param_type(self, request_data: dict, fields: dict):
        """
        批量验证参数的类型
        :param request_data: 请求的参数数据
        :param fields: {'a':str,'b':int}
        :return:
        """

        for k, v in request_data.items():
            param_type = self.verify_one_param_type(k, v, fields.get(k))
            if param_type:
                return param_type
            else:
                pass

    def verify_version(self, version, xml=None):
        """
        API版本验证
        :param version: 版本信息
        :param xml: 是否是xml
        :return:
        """
        if version == apiVersion.version1.value:
            return True, True
        else:  # 版本信息不存在给的提示
            result = response_code.REQUEST_VERSION_ISEXISTENCE
            return False, response_result_process(result, xml=xml)


req = requestProcess()
