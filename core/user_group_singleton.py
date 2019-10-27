#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: user_group_singleton.py
@create date: 2019-10-27 15:03 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from db.user_group.db_group_mgr import db_group_mgr

__all__ = ["UserGroupSingleton"]


class UserGroupSingleton:
    """
    """

    def add_user_group(self, group_name, group_desc, role_ids):
        """
        添加用户组
        :return:
        """
        return db_group_mgr.add_group(group_name, group_desc, role_ids)

    def update_user_group(self, group_json):
        """
        编辑更新用户组
        :return:
        """
        return db_group_mgr.upd_group(group_json)

    def delete_user_group(self, group_id, role_ids):
        """
        通过用户组删除用户组，并将该用户组下得所有用户移除用户组
        :param id:
        :return:
        """
        return db_group_mgr.del_group(group_id, role_ids)

    def remove_user_from_group(self, group_id, user_ids):
        """
        从用户组移除用户
        :param id:
        :return:
        """
        return db_group_mgr.remove_group_users(group_id, user_ids)

    def add_user_to_group(self, group_id, user_ids):
        """
        添加用户到用户组
        :param group_id:
        :param user_ids:
        :return:
        """
        return db_group_mgr.add_user_to_group(group_id, user_ids)

    def get_groups_list(self, current_page, page_size, search_name):
        """
        获取所有组列表
        :return:
        """
        return db_group_mgr.get_group_list(current_page, page_size, search_name)

    def get_users_by_group_id(self, group_id, current_page, page_size):
        """
        获取用户组下得所有用户
        :return:
        """
        return db_group_mgr.get_user_by_group_id(group_id, current_page, page_size)

    def get_user_group_roles(self, group_id):
        """
        获取用户组的角色信息
        :param group_id:
        :return:
        """
        return db_group_mgr.get_user_group_roles(group_id)

    def add_user_group_roles(self, group_id, role_ids):
        """
        添加用户组角色
        :param group_id:
        :param role_ids:
        :return:
        """
        return db_group_mgr.add_user_group_roles(group_id, role_ids)

    def remove_user_group_roles(self, group_id, role_ids):
        """
        删除用户组角色
        :param group_id:
        :param role_ids:
        :return:
        """
        return db_group_mgr.remove_user_group_roles(group_id, role_ids)


user_group_singleton = UserGroupSingleton()
