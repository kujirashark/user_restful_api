#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: role_permission_singleton.py
@create date: 2019-10-27 15:02 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from db.role.db_role_permission_mgr import db_role_permission

__all__ = {"rolePermissionSingleton"}


class rolePermissionSingleton:
    """
    """

    def get_user_permission_info(self):
        """
        获取所有的权限信息
        :return:
        """
        return db_role_permission.get_user_permission_info()

    def get_data_permission_info(self):
        """
        获取所有的权限信息
        :return:
        """
        return db_role_permission.get_data_permission_info()

    def get_all_roles(self):
        """
        获取所有的角色信息
        :return:
        """
        return db_role_permission.get_all_roles()

    def get_pages_roles(self, current_page, page_size, search_data):
        """
        获取所有的角色信息
        :return:
        """
        return db_role_permission.get_pages_roles(current_page, page_size, search_data)

    def add_role(self, role_name, note_info):
        """
        添加角色
        :param role_name: 角色名称
        :param note_info: 备注信息
        :return:
        """
        return db_role_permission.add_role(role_name, note_info)

    def update_role(self, role_id, role_name, note_info):
        """
        修改角色
        :param role_id: 角色ID
        :param role_name: 角色名称
        :param note_info: 备注信息
        :return:
        """
        return db_role_permission.update_role(role_id, role_name, note_info)

    def delete_role(self, role_id):
        """
        删除角色
        :param role_id:
        :return:
        """
        return db_role_permission.delete_role(role_id)

    def add_role_permission(self, role_id, per_keys):
        """
        给角色添加权限
        :param role_id: 角色id
        :param per_keys: 权限列表
        :return:
        """
        return db_role_permission.add_role_permission(role_id, per_keys)

    def get_role_permission_info(self, role_id):
        """
        根据角色ID获取权限列表
        :param role_id: 角色ID
        :return:
        """
        return db_role_permission.get_role_permission_info(role_id)

    def add_grafana_permission(self, param):
        """

        :param param:
        :return:
        """
        return db_role_permission.add_grafana_permission(param)

    def get_grafana_permission(self, user_id):
        """
        获取grafana权限
        :param param:
        :return:
        """
        return db_role_permission.get_grafana_permission(user_id)


role_permission_singleton = rolePermissionSingleton()
