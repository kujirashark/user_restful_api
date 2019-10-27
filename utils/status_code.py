#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: status_code.py
@create date: 2019-10-27 14:21 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""


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


response_code = responseCode()
