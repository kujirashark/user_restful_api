#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: db_department_mgr.py
@create date: 2019-10-27 15:05 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn

from db.user.db_user_mgr import user_mgr

from utils.status_code import response_code
from utils.log_helper import lg


class DbDepartmentMgr(DbBase):
    def get_all_department(self):
        """
        获取所有的部门信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'department'
            fields = 'dpt_id,dpt_name,p_id'
            sql = self.create_select_sql(db_name, table_name, fields)
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_department(self, dpt_name, dpt_p_id):
        """
        添加部门
        :param dpt_name: 部门名称
        :param dpt_p_id: 上级部门id
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'department'
            filed = 'dpt_name'
            condition = "dpt_name = '%s'" % dpt_name
            system_name_sql = DbBase.create_select_sql(self, db_name, table_name, filed, condition)
            res = DbBase.execute_fetch_one(self, db_conn, system_name_sql)
            if res:
                return response_code.RECORD_EXIST
            else:
                fields = '(dpt_name, p_id)'
                pla_data = (dpt_name, dpt_p_id)
                sql = DbBase.create_insert_sql(self, db_name, table_name, fields, pla_data)
                DbBase.execute_sql_return_count(self, db_conn, sql)
                return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def update_department(self, dpt_id, dpt_name, p_id):
        """
        修改部门
        :param dpt_id:  部门ID
        :param dpt_name:  部门名称
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'department'
            filed = 'dpt_name'
            condition = "dpt_id <> %s and dpt_name = '%s'" % (dpt_id, dpt_name)
            old_sql = DbBase.create_select_sql(self, db_name, table_name, filed, condition)
            old_pla_name_data = DbBase.execute_fetch_one(self, db_conn, old_sql)
            if old_pla_name_data:
                return response_code.RECORD_EXIST
            else:
                fields = ['dpt_id', 'dpt_name', 'p_id']
                pla_data = [dpt_id, dpt_name, p_id]
                update_condition = 'dpt_id = %s' % str(dpt_id)
                update_sql = DbBase.create_update_sql(self, db_name, table_name, fields, pla_data, update_condition)
                DbBase.execute_update_sql(self, db_conn, update_sql)
                return response_code.SUCCESS
        except Exception as  e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def delete_department(self, dpt_id):
        """
        删除部门
        :param dpt_id:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = "department"
            user_dpt_table = "users_department"
            filed = 'dpt_id'
            condition = "dpt_id = %s " % dpt_id
            old_sql = self.create_select_sql(db_name, user_dpt_table, filed, condition)
            # 获取用户和部门管理表的数据
            old_dpt_data = self.execute_fetch_one(db_conn, old_sql)
            if old_dpt_data:
                condition = "dpt_id=%s" % old_dpt_data.get('dpt_id')
                del_association_sql = self.create_delete_sql(db_name, user_dpt_table, condition)
                # 删除用户和部门关联表的数据
                self.execute_del_data(db_conn, del_association_sql)
            # 删除部门数据
            condition = "dpt_id=%s" % dpt_id
            sql = self.create_delete_sql(db_name, table_name, condition)
            self.execute_del_data(db_conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()

    def get_dpt_user_info_by_id(self, dpt_id, current_page, page_size):
        """
        获取部门下的员工信息
        :param dpt_id:
        :param current_page:
        :param page_size:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'users_department'
            fields = 'user_id'
            condition = 'dpt_id=%s' % dpt_id
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data_list = result.get('data_list')
            if data_list:
                user_data = tuple([user.get('user_id') for user in data_list])
                user_data_list = user_mgr.get_user_by_ids(user_data)
            else:
                user_data_list = []
            data = response_code.SUCCESS
            data['data'] = user_data_list
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def department_add_staff(self, dpt_id, user_ids):
        """
        给部门下面添加员工
        :param dpt_id: 部门ID
        :param user_ids: 员工ID
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'users_department'
            for user_id in eval(user_ids):
                condition = "user_id =%s and dpt_id=%s" % (user_id, dpt_id)
                is_exist_sql = self.create_select_sql(db_name, table_name, "*", condition)
                res = self.execute_fetch_one(db_conn, is_exist_sql)
                if res:
                    continue
                fields = '(user_id,dpt_id)'
                value_tuple = (user_id, dpt_id)
                insert_user_sql = self.create_insert_sql(db_name, table_name, fields, value_tuple)
                self.insert_exec(db_conn, insert_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def delete_department_staff(self, dpt_id, user_ids):
        """
        删除部门下的员工信息
        :param dpt_id: 部门ID
        :param user_ids:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'users_department'
            for user_id in eval(user_ids):
                condition = "user_id=%s and dpt_id = %s" % (user_id, dpt_id)
                sql = self.create_delete_sql(db_name, table_name, condition)
                # 删除部门员工
                self.execute_del_data(db_conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()

    def update_department_staff(self, dpt_id, user_ids):
        """
        给部门下面添加员工
        :param dpt_id: 部门ID
        :param user_ids: 员工ID
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'users_department'
            filed = 'dpt_id'
            condition = "dpt_id = %s " % dpt_id
            old_sql = self.create_select_sql(db_name, table_name, filed, condition)
            # 获取用户和部门管理表的数据
            old_dpt_data = self.execute_fetch_one(db_conn, old_sql)
            if old_dpt_data:
                condition = "dpt_id=%s" % old_dpt_data.get('dpt_id')
                del_association_sql = self.create_delete_sql(db_name, table_name, condition)
                # 删除旧的用户和部门关联表的数据
                self.execute_del_data(db_conn, del_association_sql)
            # 添加新的员工
            for user_id in eval(user_ids):
                fields = '(dpt_id,user_id)'
                insert_data = (dpt_id, user_id)
                sql = DbBase.create_insert_sql(self, db_name, table_name, fields, insert_data)
                DbBase.execute_sql_return_count(self, db_conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()


db_department_mgr = DbDepartmentMgr()
