#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: department_singleton.py
@create date: 2019-10-27 15:01 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from db.department.db_department_mgr import db_department_mgr

__all__ = {"departmentSingleton"}


class departmentSingleton():

    def get_department(self):
        """
        获取所有的部门信息
        :return:
        """
        return db_department_mgr.get_all_department()

    def add_department(self, dpt_name, dpt_p_id):
        """
        添加部门
        :param dpt_name: 部门名称
        :param dpt_p_id: 上级部门id
        :return:
        """
        return db_department_mgr.add_department(dpt_name, dpt_p_id)

    def update_department(self, dpt_id, dpt_name, p_id):
        """
        修改部门
        :param dpt_id:  部门ID
        :param dpt_name:  部门名称
        :return:
        """
        return db_department_mgr.update_department(dpt_id, dpt_name, p_id)

    def delete_department(self, dpt_id):
        """
        删除部门
        :param dpt_id: 部门ID
        :return:
        """
        return db_department_mgr.delete_department(dpt_id)

    def get_dpt_user_info_by_id(self, dpt_id, current_page, page_size):
        """
        获取部门下的员工信息
        :param dpt_id:
        :param current_page:
        :param page_size:
        :return:
        """
        return db_department_mgr.get_dpt_user_info_by_id(dpt_id, current_page, page_size)

    def department_add_staff(self, dpt_id, user_ids):
        """
        给部门下面添加员工
        :param dpt_id:
        :param user_ids:
        :return:
        """
        return db_department_mgr.department_add_staff(dpt_id, user_ids)

    def delete_department_staff(self, dpt_id, user_ids):
        """
        删除部门下的员工信息
        :param dpt_id:
        :param user_ids:
        :return:
        """
        return db_department_mgr.delete_department_staff(dpt_id, user_ids)

    def update_department_staff(self, dpt_id, user_ids):
        """
        删除部门下的员工信息
        :param dpt_id:
        :param user_ids:
        :return:
        """
        return db_department_mgr.update_department_staff(dpt_id, user_ids)


department_singleton = departmentSingleton()
