#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: db_group_mgr.py
@create date: 2019-10-27 15:09 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from common.common_time import get_system_datetime
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn

from db.user.db_user_mgr import user_mgr
from utils.log_helper import lg
from utils.status_code import response_code


class DBGroupMgr(DbBase):
    """
    用户组管理类
    """

    def get_group_list(self, current_page, page_size, search_name):
        """
        分页查询用户组信息
        :param current_page:
        :param page_size:
        :param search_name:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            start_num = (current_page - 1) * page_size
            # 添加查询条件
            condition = None
            if search_name:
                search_condition = search_name
                for key in search_condition.keys():
                    condition = key + ' like "%' + search_condition[key] + '%"'
            user_group_fields = 'id,name,description,create_time'
            sql_count, sql = self.create_get_page_sql(db_name, 'user_group', user_group_fields, start_num, page_size,
                                                      condition=condition)
            groups_result = self.execute_fetch_pages(conn, sql_count, sql, current_page, page_size)
            for group in groups_result["data_list"]:
                # 用户组角色查询
                group_id = group.get('id')
                role_relations = [
                    {"table_name": "user_group_role", "join_condition": "user_group_role.role_id=role.id"}]
                condition = "user_group_role.group_id=" + str(group_id)
                role_query_sql = self.create_get_relation_sql(db_name, "role", "id,name", role_relations,
                                                              condition=condition)
                roles = self.execute_fetch_all(conn, role_query_sql)
                role_name_str = ''
                role_ids = []
                if len(roles) == 0:
                    pass
                elif len(roles) == 1:
                    role_name_str = roles[0]["name"]
                    role_ids.append(roles[0]["id"])
                else:
                    for role in roles:
                        role_name_str += role["name"] + '|'
                        role_ids.append(role["id"])
                group["roles"] = role_name_str.rstrip('|')
                group["role_ids"] = role_ids
            # 返回
            data = response_code.SUCCESS
            data["data"] = groups_result.get('data_list')
            data["total"] = groups_result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:

            conn.close()

    def get_all_groups(self):
        """
        获取所有用户组
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_group'
            fields = 'id,name,description as desc,create_time'
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

    def get_user_group_by_name(self, group_name):
        """
        通过名称查询用户组信息
        :param group_name:
        :return:
        """
        conn = MysqlConn()
        try:
            condition = 'name="%s"' % group_name
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'user_group', 'id', condition=condition)
            return self.execute_fetch_one(conn, sql)
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def add_group(self, group_name, group_desc, role_ids):
        """
        添加用户组
        :param group_name:
        :param group_desc:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_group'
            filed = 'name'
            condition = "name = '%s'" % group_name
            is_exist_sql = self.create_select_sql(db_name, table_name, filed, condition)
            res = self.execute_fetch_one(db_conn, is_exist_sql)
            if res:
                return response_code.RECORD_EXIST
            fields = '(name,description,create_time)'
            create_time = get_system_datetime()
            value_tuple = (group_name, group_desc, create_time)
            insert_user_sql = self.create_insert_sql(db_name, table_name, fields, value_tuple)
            self.insert_exec(db_conn, insert_user_sql)
            # 查询新添加的用户组
            new_group = self.get_user_group_by_name(group_name)
            new_group_id = new_group.get('id')
            # 添加用户组的角色
            group_role_fields = '(group_id,role_id)'
            for role_id in eval(str(role_ids)):
                group_role_value_tuple = (new_group_id, role_id)
                insert_user_sql = self.create_insert_sql(db_name, "user_group_role", group_role_fields,
                                                         group_role_value_tuple)
                self.insert_exec(db_conn, insert_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def del_group(self, group_id, role_ids):
        """
        删除用户组
        :param group_id:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # 关闭外键检测
            # db_conn.cur.execute('SET FOREIGN_KEY_CHECKS = 0;')
            # db_conn.conn.commit()
            # 删除用户组角色
            for role_id in eval(str(role_ids)):
                condition = "group_id=%s and role_id=%s" % (group_id, role_id)
                delete_group_role_sql = self.create_delete_sql(db_name, "user_group_role", condition)
                self.delete_exec(db_conn, delete_group_role_sql)
            # 删除用户组下所有用户
            condition = "group_id=%s" % group_id
            delete_group_user_sql = self.create_delete_sql(db_name, "user_user_group", condition)
            self.delete_exec(db_conn, delete_group_user_sql)
            # 删除用户组主表信息
            table_name = 'user_group'
            condition = "id=%s" % group_id
            delete_group_sql = self.create_delete_sql(db_name, table_name, condition)
            self.delete_exec(db_conn, delete_group_sql)

            # 开起外键检测
            # db_conn.cur.execute('SET FOREIGN_KEY_CHECKS = 1;')
            # db_conn.conn.commit()
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()

    def upd_group(self, group_json):
        """
        更新用户组
        :param group_json:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # 解析参数成dict
            group = group_json
            table_name = 'user_group'
            condition = "id=%s" % group.get('id')
            # 更新用户基本信息
            update_group_fields = ['name', 'description']
            update_group_fields_value = [group.get('name'), group.get('desc')]
            update_group_sql = self.create_update_sql(db_name, table_name, update_group_fields,
                                                      update_group_fields_value,
                                                      condition)
            self.updete_exec(db_conn, update_group_sql)
            # 删除用户组原有角色
            condition = "group_id=%s" % group.get('id')
            delete_group_role_sql = self.create_delete_sql(db_name, "user_group_role", condition)
            self.delete_exec(db_conn, delete_group_role_sql)

            # 添加用户组的角色
            group_role_fields = '(group_id,role_id)'
            for role_id in eval(str(group.get('role_ids'))):
                group_role_value_tuple = (group.get('id'), role_id)
                insert_group_role_sql = self.create_insert_sql(db_name, "user_group_role", group_role_fields,
                                                               group_role_value_tuple)
                self.insert_exec(db_conn, insert_group_role_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def add_user_to_group(self, group_id, user_ids):
        """
        添加用户到用户组
        :param group_id:用户组id
        :param user_ids:用户id列表
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_user_group'
            for user_id in eval(user_ids):
                condition = "user_id =%s and group_id=%s" % (user_id, group_id)
                is_exist_sql = self.create_select_sql(db_name, table_name, "*", condition)
                res = self.execute_fetch_one(db_conn, is_exist_sql)
                if res:
                    continue
                fields = '(user_id,group_id)'
                value_tuple = (user_id, group_id)
                insert_user_sql = self.create_insert_sql(db_name, table_name, fields, value_tuple)
                self.insert_exec(db_conn, insert_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def remove_group_users(self, group_id, user_ids):
        """
        移除用户组内的用户
        :param group_id:
        :param user_ids:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_user_group'
            for user_id in eval(user_ids):
                condition = "user_id =%s and group_id=%s" % (user_id, group_id)
                is_exist_sql = self.create_select_sql(db_name, table_name, "*", condition)
                res = self.execute_fetch_one(db_conn, is_exist_sql)
                if res:
                    del_user_sql = self.create_delete_sql(db_name, table_name, condition)
                    self.delete_exec(db_conn, del_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()

    def get_user_by_group_id(self, group_id, current_page, page_size):
        """
        查询用户组下所有用户
        :param group_id:
        :param current_page:
        :param page_size:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_num = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'user_user_group'
            fields = 'user_id'
            condition = 'group_id=%s' % group_id
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_num, page_size, condition)
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data_list = result.get('data_list')

            if data_list:
                user_data = tuple([user.get('user_id') for user in data_list])
                user_data_list = user_mgr.get_user_by_ids(user_data)
            else:
                user_data_list = []

            # user_data = tuple([user.get('user_id') for user in data])
            # user_data_list = user_mgr.get_user_by_ids(user_data)
            data = response_code.SUCCESS
            data['data'] = user_data_list
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_user_group_roles(self, group_id):
        """
        获取用户组的角色信息
        :param group_id:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_group_role'
            fields = 'role_id'
            condition = 'group_id=%s' % group_id
            sql = self.create_select_sql(db_name, table_name, fields, condition=condition)
            result = self.execute_fetch_all(db_conn, sql)
            if result:
                role_ids = tuple([role.get('role_id') for role in result])
                if len(role_ids) == 1:
                    role_condition = 'id=%s' % role_ids[0]
                else:
                    role_condition = 'id in %s' % str(role_ids)
                sql = self.create_select_sql(db_name, 'role', '*', condition=role_condition)
                role_result = self.execute_fetch_all(db_conn, sql)
                data = response_code.SUCCESS
                data['data'] = role_result
            else:
                data = response_code.SUCCESS
                data['data'] = []
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_user_group_roles(self, group_id, role_ids):
        """
        添加用户组角色
        :param group_id:
        :param role_ids:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_group_role'
            for role_id in eval(role_ids):
                condition = "role_id =%s and group_id=%s" % (role_id, group_id)
                is_exist_sql = self.create_select_sql(db_name, table_name, "*", condition)
                res = self.execute_fetch_one(db_conn, is_exist_sql)
                if res:
                    continue
                fields = '(role_id,group_id)'
                value_tuple = (role_id, group_id)
                insert_user_sql = self.create_insert_sql(db_name, table_name, fields, value_tuple)
                self.insert_exec(db_conn, insert_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def remove_user_group_roles(self, group_id, role_ids):
        """
        移除用户组的角色
        :param group_id:
        :param role_ids:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'user_group_role'
            for role_id in eval(role_ids):
                condition = "role_id =%s and group_id=%s" % (role_id, group_id)
                is_exist_sql = self.create_select_sql(db_name, table_name, "*", condition)
                res = self.execute_fetch_one(db_conn, is_exist_sql)
                if res:
                    del_user_sql = self.create_delete_sql(db_name, table_name, condition)
                    self.delete_exec(db_conn, del_user_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()


db_group_mgr = DBGroupMgr()
