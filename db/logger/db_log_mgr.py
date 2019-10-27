#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: db_log_mgr.py
@create date: 2019-10-27 14:45 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
import json

from common.common_time import get_system_datetime
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn

from utils.log_helper import lg
from utils.status_code import response_code


class DbLogMgr(DbBase):
    """
    日志相关数据库表操作类
    """

    def get_pages_operation_log(self, current_page, page_size, search_data, time_scope):
        """
        获取日志信息
        :param current_page:
        :param page_size:
        :param search_data:
        :param time_scope:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'system_oper_log'
            fields = 'log_key, (select name from %s.users where  id = user_key) as user_name,user_key,ip_address,level,description,time_create' % db_name

            condition = ''
            # 给定了查询字段
            if len(json.loads(search_data)) > 0:
                condition = self.create_vague_condition_sql(search_data)
            # 给定了查询时间类型
            if time_scope:
                time_scope = eval(time_scope)
                start_time = time_scope[0]
                end_time = time_scope[1]
                if condition:
                    condition += ' and time_create between ' + str(start_time) + ' and ' + str(end_time)
                else:
                    condition += 'time_create between ' + str(start_time) + ' and ' + str(end_time)
            condition += ' order by time_create desc'
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_operation_log(self, user_key, ip_address, level, description):
        """
        添加操作日志
        :param user_key:
        :param ip_address:
        :param level:
        :param description:
        :return:
        """
        db_conn = MysqlConn()
        time_create = get_system_datetime()
        db_name = configuration.get_database_name()
        table_name = 'system_oper_log'
        fields = '(user_key,ip_address,level,description,time_create)'
        pla_data = (user_key, ip_address, level, description, time_create)
        sql = DbBase.create_insert_sql(self, db_name, table_name, fields, pla_data)
        DbBase.execute_sql_return_count(self, db_conn, sql)
        db_conn.close()

    def get_pages_system_log(self, current_page, page_size, search_data, time_scope):
        """
        分页查询系统日志
        :param current_page:
        :param page_size:
        :param search_data:
        :param time_scope:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'system_log'
            fields = 'log_key,title,source,ip_address,level,status,' \
                     'opinion,opinion_user,opinion_time,time_create,description'
            condition = ''
            # 给定了查询字段
            if len(json.loads(search_data)) > 0:
                condition = self.create_vague_condition_sql(search_data)
            # 给定了查询时间类型
            if time_scope:
                time_scope = eval(time_scope)
                start_time = time_scope[0]
                end_time = time_scope[1]
                if condition:
                    condition += ' and TIME_CREATE between ' + str(start_time) + ' and ' + str(end_time)
                else:
                    condition += 'TIME_CREATE between ' + str(start_time) + ' and ' + str(end_time)
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            # 执行查询
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def update_system_log(self, log_key, opinion, opinion_user, status):
        """
        处理后，修改日志信息
        :param log_key:日志id
        :param opinion:处理意见
        :param opinion_user:处理人
        :param status:状态
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'system_log'
            condition = "log_key=%s" % log_key
            # 查看状态是否已经更新
            sql = self.create_select_sql(db_name, table_name, 'status', condition)
            log = self.execute_fetch_one(db_conn, sql)
            if log.get('status') == 2:
                return response_code.ALREADY_HANDLED
            # 更新日志信息
            opinion_time = get_system_datetime()
            update_group_fields = ['opinion', 'opinion_user', 'status', 'opinion_time']
            update_group_fields_value = [opinion, opinion_user, status, opinion_time]
            update_group_sql = self.create_update_sql(db_name, table_name, update_group_fields,
                                                      update_group_fields_value,
                                                      condition)
            self.updete_exec(db_conn, update_group_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def get_pages_message(self, user_id, current_page, page_size, search_data):
        """
        分页查询系统消息
        :param user_id:
        :param current_page:
        :param page_size:
        :param search_data:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            fields = 'id,title,content,create_time,status'
            condition = "user_id=%s" % user_id
            # 给定了查询字段
            if search_data:
                condition += ' and ' + self.create_vague_condition_sql(search_data)
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            # 执行查询
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            print(sql)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def update_message_status(self, id_list):
        """
        修改系统消息状态
        :param message_id:
        :return:
        """
        db_conn = MysqlConn()
        try:

            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            for message_id in eval(id_list):
                condition = "id=%s" % message_id
                # 更新系统信息
                update_fields = ['state']
                update_fields_value = [1]
                update_sql = self.create_update_sql(db_name, table_name, update_fields, update_fields_value, condition)

                self.updete_exec(db_conn, update_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def get_message_count(self, creator):
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            data = response_code.SUCCESS
            fields = 'id,title,content,create_time,state'
            condition = " state = 0"
            # 给定了查询字段
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, 0, 9000000, condition)
            # 执行查询
            result = self.execute_fetch_pages(db_conn, sql_count, sql, 1, 9000000)
            data['data'] = result

            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()


db_log = DbLogMgr()
