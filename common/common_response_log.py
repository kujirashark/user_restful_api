#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: common_response_log.py
@create date: 2019-10-27 14:11 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：响应日志处理
"""

class ResponseLog:
    """
    响应提示信息公共类
    """

    @staticmethod
    def null_value(param):
        """
        参数值为空时，提示信息
        :param param:
        :return:
        """
        return "param '%s' is null ." % (param)

    @staticmethod
    def wrong_value(param, value):
        """
        参数值无效时，提示信息
        :param param:
        :param value:
        :return:
        """
        return "param '%s' improper value %s." % (param, value)

    @staticmethod
    def record_exist(unique_key, value):
        """
        参数值已经存在时，提示信息
        :param unique_key:
        :param value:
        :return:
        """
        return "unique key '(%s,%s)' is exist." % (unique_key, value)

    @staticmethod
    def delete_record_in_use(code, value):
        """
        删除的数据在使用时，提示信息
        :param code:
        :param value:
        :return:
        """
        return "delete record '%s:%s' is in use." % (code, value)

    @staticmethod
    def wrong_time_format(key, value):
        """
        时间格式错误，提示信息
        :param key: 字段名称
        :param value: 时间戳
        :return:
        """
        return "improper time format: param '%s:[%s]'." % (key, value)

    @staticmethod
    def wrong_param_type(key, value):
        """
        参数类型错误提示消息
        :param key: 参数名称
        :param value: 参数类型
        :return:
        """
        return "The argument '%s must be %s'." % (key, value)

    @staticmethod
    def wrong_param_must(key):
        """
        验证参数是否必填
        :param key:
        :return:
        """
        return "The argument '" + key + "' is missed."

    @staticmethod
    def database_exception(error_code=None):
        """
        数据库操作异常，提示信息
        :return:
        """
        if error_code:
            if error_code == 1022:
                msg = "Failure of database connection."
            elif error_code == 1024:
                msg = "Database operation exception."
            else:
                msg = ""
            return msg
        else:
            return ""

    @staticmethod
    def operation_success(data_name=None, operation_name=None):
        """
        添加数据成功，提示消息
        :param data_name:
        :param operation_name:
        :return:
        """
        return "%s data %s success." % (data_name, operation_name)

    @staticmethod
    def record_not_exist(data, value):
        """
        数据不存在，提示消息
        :param data:
        :param value:
        :return:
        """
        return "Data '(%s,%s)' is  not exist." % (data, value)

    @staticmethod
    def mission_db_exist(sat_code):
        """
        与卫星代号同名的任务数据库存在，提示消息
        :param sat_code:
        :return:
        """
        return "Mission db with this '%s' name already exists" % (sat_code)

    @staticmethod
    def relation_not_exist(v1, v2):
        """
        数据关联关系不存在，提示消息
        :param data:
        :param value:
        :return:
        """
        return "Relationship between '(%s,%s)' is  not exist." % (v1, v2)
