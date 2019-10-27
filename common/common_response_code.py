#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: common_response_code.py
@create date: 2019-10-27 14:10 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from enum import Enum, unique


@unique
class ErrorCodeEnum(Enum):
    SUCCESS = 200
    LOGIN_IS_FAIL = 1001
    PASS_WORD_INFO_NOT_FILL = 1002
    TWO_PASS_WORD_DIFFERENT = 1003
    OLD_PASS_WORD_IS_NOT_FAIL = 1004
    LOGIN_FAIL = 1005
    PASS_WORD_RESET_FAIL = 1006
    USER_NOT_EXIST = 1007
    IMPORT_CSV_FAIL = 1008
    IMPORT_CSV_SUCCESS = 1009
    RECORD_EXIST = 1010
    ADD_DATA_FAIL = 1011
    UPDATE_DATA_FAIL = 1012
    DELETE_DATA_FAIL = 1013
    GET_DATA_FAIL = 1014
    REQUEST_VERSION_ISEXISTENCE = 1015
    ALREADY_HANDLED = 1016
    DATA_IS_NOT_EXIST = 1017
    REQUEST_PARAM_MISSED = 1018
    EQUEST_PARAM_FORMAT_ERROR = 1019
    OPENTSDB_ERROR = 1020
    DATA_BASE_ERROR = 1021
    NOT_FOUND = 404
    BAD_REQUEST = 400
    FORBIDDEND = 403
    WRONGVALUE = 1022
    CHECK_EXIST_ERROR = 1023
    EXCEPTION_DB = 1024


class responseCode(object):

    @property
    def SUCCESS(self):
        return {'code': 200, 'msg': '请求成功'}

    @property
    def LOGIN_IS_FAIL(self):
        return {'code': 1001, 'msg': '用户名或者密码错误'}

    @property
    def PASS_WORD_INFO_NOT_FILL(self):
        return {'code': 1002, 'msg': '密码信息填写完整'}

    @property
    def TWO_PASS_WORD_DIFFERENT(self):
        return {'code': 1003, 'msg': '两次密码不一致'}

    @property
    def OLD_PASS_WORD_IS_NOT_FAIL(self):
        return {'code': 1004, 'msg': '旧密码不正确'}

    @property
    def LOGIN_FAIL(self):
        return {'code': 1005, 'msg': '登录失败请联系管理员'}

    @property
    def PASS_WORD_RESET_FAIL(self):
        return {'code': 1006, 'msg': '密码重置失败'}

    @property
    def USER_NOT_EXIST(self):
        return {'code': 1007, 'msg': '用户不存在'}

    @property
    def IMPORT_CSV_FAIL(self):
        return {'code': 1008, 'msg': '导入数据失败'}

    @property
    def IMPORT_CSV_SUCCESS(self):
        return {'code': 1009, 'msg': '导入数据成功'}

    @property
    def RECORD_EXIST(self):
        return {'code': 1010, 'msg': '记录已存在'}

    @property
    def ADD_DATA_FAIL(self):
        return {'code': 1011, 'msg': '添加数据失败'}

    @property
    def UPDATE_DATA_FAIL(self):
        return {'code': 1012, 'msg': '修改数据失败'}

    @property
    def DELETE_DATA_FAIL(self):
        return {'code': 1013, 'msg': '删除数据失败'}

    @property
    def GET_DATA_FAIL(self):
        return {'code': 1014, 'msg': '获取数据失败'}

    @property
    def REQUEST_VERSION_ISEXISTENCE(self):
        return {'code': 1015, 'msg': '请求的版本不存在'}

    @property
    def ALREADY_HANDLED(self):
        return {'code': 1016, 'msg': '参数类型错误'}

    @property
    def DATA_IS_NOT_EXIST(self):
        return {'code': 1017, 'msg': '数据不存在'}

    @property
    def REQUEST_PARAM_MISSED(self):
        return {'code': 1018, 'msg': '请求参数缺失'}

    @property
    def REQUEST_PARAM_FORMAT_ERROR(self):
        return {'code': 1019, 'msg': '请求参数格式错误'}

    @property
    def OPENTSDB_ERROR(self):
        return {'code': 1020, 'msg': 'opentsdb服务器错误'}

    @property
    def DATA_BASE_ERROR(self):
        return {'code': 1021, 'msg': "数据库连接失败"}

    @property
    def NOT_FOUND(self):
        return {'code': 404, 'msg': 'HTTP 404 Not Found'}

    @property
    def BAD_REQUEST(self):
        return {'code': 400, 'msg': 'HTTP 400 Bad Request'}

    @property
    def FORBIDDEND(self):
        return {'code': 403, 'msg': 'HTTP 403 Forbidden'}

    @property
    def WRONGVALUE(self):
        return {'code': 1022, 'msg': '参数值超出规定范围'}

    @property
    def CHECK_EXIST_ERROR(self):
        return {'code': 1023, 'msg': '验证数据错误'}

    @property
    def EXCEPTION_DB(self):
        return {'code': 1024, 'msg': '数据库操作异常'}

    def get_struct_by_error_code(self, error_code):
        if error_code == ErrorCodeEnum.SUCCESS:
            return self.SUCCESS
        if error_code == ErrorCodeEnum.LOGIN_IS_FAIL:
            return self.LOGIN_IS_FAIL
        if error_code == ErrorCodeEnum.PASS_WORD_INFO_NOT_FILL:
            return self.PASS_WORD_INFO_NOT_FILL
        if error_code == ErrorCodeEnum.TWO_PASS_WORD_DIFFERENT:
            return self.TWO_PASS_WORD_DIFFERENT
        if error_code == ErrorCodeEnum.OLD_PASS_WORD_IS_NOT_FAIL:
            return self.OLD_PASS_WORD_IS_NOT_FAIL
        if error_code == ErrorCodeEnum.LOGIN_FAIL:
            return self.LOGIN_FAIL
        if error_code == ErrorCodeEnum.PASS_WORD_RESET_FAIL:
            return self.PASS_WORD_RESET_FAIL
        if error_code == ErrorCodeEnum.USER_NOT_EXIST:
            return self.PASS_WORD_RESET_FAIL
        if error_code == ErrorCodeEnum.IMPORT_CSV_FAIL:
            return self.IMPORT_CSV_FAIL
        if error_code == ErrorCodeEnum.IMPORT_CSV_SUCCESS:
            return self.IMPORT_CSV_SUCCESS
        if error_code == ErrorCodeEnum.RECORD_EXIST:
            return self.RECORD_EXIST
        if error_code == ErrorCodeEnum.ADD_DATA_FAIL:
            return self.ADD_DATA_FAIL
        if error_code == ErrorCodeEnum.UPDATE_DATA_FAIL:
            return self.UPDATE_DATA_FAIL
        if error_code == ErrorCodeEnum.DELETE_DATA_FAIL:
            return self.DELETE_DATA_FAIL
        if error_code == ErrorCodeEnum.GET_DATA_FAIL:
            return self.DELETE_DATA_FAIL
        if error_code == ErrorCodeEnum.REQUEST_VERSION_ISEXISTENCE:
            return self.REQUEST_VERSION_ISEXISTENCE
        if error_code == ErrorCodeEnum.ALREADY_HANDLED:
            return self.ALREADY_HANDLED
        if error_code == ErrorCodeEnum.DATA_IS_NOT_EXIST:
            return self.DATA_IS_NOT_EXIST
        if error_code == ErrorCodeEnum.REQUEST_PARAM_MISSED:
            return self.REQUEST_PARAM_MISSED
        if error_code == ErrorCodeEnum.REQUEST_PARAM_FORMAT_ERROR:
            return self.REQUEST_PARAM_FORMAT_ERROR
        if error_code == ErrorCodeEnum.OPENTSDB_ERROR:
            return self.OPENTSDB_ERROR
        if error_code == ErrorCodeEnum.DATA_BASE_ERROR:
            return self.DATA_BASE_ERROR
        if error_code == ErrorCodeEnum.NOT_FOUND:
            return self.NOT_FOUND
        if error_code == ErrorCodeEnum.BAD_REQUEST:
            return self.BAD_REQUEST
        if error_code == ErrorCodeEnum.FORBIDDEND:
            return self.FORBIDDEND
        if error_code == ErrorCodeEnum.WRONGVALUE:
            return self.WRONGVALUE
        if error_code == ErrorCodeEnum.CHECK_EXIST_ERROR:
            return self.CHECK_EXIST_ERROR
        if error_code == ErrorCodeEnum.EXCEPTION_DB:
            return self.EXCEPTION_DB


response_code = responseCode()
