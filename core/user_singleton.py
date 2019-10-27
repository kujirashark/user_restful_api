#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: user_singleton.py
@create date: 2019-10-27 15:03 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from db.user.db_user_mgr import user_mgr

__all__ = {"UserSingleton"}


class UserSingleton:
    """"
    """

    def get_users_info(self, page, page_num, search_data=None):
        """
        获取所有用户信息
        :return:返回用户信息json
        """

        return user_mgr.get_user_list(page, page_num, search_data)

    def get_user_info_by_id(self, id):
        """
        通过用户ID获取用户信息
        :param id: 用户id
        :return: 返回当前用户JSON
        """
        return user_mgr.get_user_by_id_(id)

    def get_user_role_by_id(self, id):
        """
        通过ID获取用户角色
        :param id:用户ID
        :return:返回用户权限JSON
        """

    def delete_user_by_id(self):
        """
        通过用户ID删除用户
        :return:返回成功失败
        """

    def set_default_password_by_id(self, id):
        """
        通过用户ID设置用户得默认密码
        :param id:
        :return:
        """

    def add_user(self, user_info):
        """
        添加用户
        :param user_info:
        :return:
        """

        return user_mgr.add_user(user_info)

    def update_user(self, user_info):
        """
        更新用户
        :param userinfo:
        :return:
        """
        return user_mgr.upd_user(user_info)

    def user_login(self, username, password):
        """
        用户登录验证，如果正确返回用户ID，如果不正确返回0
        :param username: 用户名
        :param password: 用户密码
        :return: 正确返回用户ID，如果不正确返回0
        """

    def reset_password(self, user_id):
        """
        重置密码
        :param user_id:
        :return:
        """
        return user_mgr.pwd_reset(user_id)

    def update_user_password(self, user_id, old_pwd, new_pwd):
        """
        修改用户密码
        :return:
        """
        return user_mgr.pwd_modify(user_id, old_pwd, new_pwd)

    def update_header_user_info(self, ser_info):
        """
        更新用户指定的信息
        :param ser_info:
        :return:
        """
        return user_mgr.upd_user_partial(ser_info)

    def get_all_users(self):
        """
        获取所有的用户信息
        :return:
        """
        return user_mgr.get_all_user()

    def delete_user(self, user_ids):
        """
        删除用户
        :param user_id:
        :return:
        """
        return user_mgr.del_user(user_ids)


user_singleton = UserSingleton()
