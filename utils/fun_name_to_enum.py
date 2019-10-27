#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: fun_name_to_enum.py
@create date: 2019-10-27 14:41 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from enum import Enum, unique


@unique
class functionName(Enum):
    # 通用的
    success = '成功'
    fail = '失败'

    get_version = '获取系统版本信息'

    """
    用户管理
    """
    # ===================================== 用户管理 start =======================================
    login = '用户登录'
    logout = '退出登录'
    get_users = '分页获取所有用户数据'
    get_user_info_by_id = '获取单个用户数据'
    add_user = '添加用户'
    update_user = '修改用户'
    delete_user = '删除用户'
    reset_password = '重置密码'
    update_user_password = '修改用户密码'
    get_all_users = '获取所有用户数据'
    update_header_user_info = '修改基本资料'
    # ===================================== 用户管理 end   ========================================

    # ===================================== 用户组管理 start =======================================
    get_user_groups = '获取所有的用户组数据'
    get_pages_user_group = '分页获取用户组数据'
    get_user_group_role_by_id = '获取用户组的角色数据'
    add_user_group = '添加用户组'
    delete_user_group = '删除用户组'
    update_user_group = '修改用户组'
    get_user_group_user_by_id = '获取用户组下面的员工数据'
    add_user_group_staff = '用户组增加人员'
    del_user_group_staff = '用户组移除人员'
    add_user_group_roles = '添加用户组角色'
    remove_user_group_roles = '删除用户组角色'

    # ===================================== 用户组管理  end  ============================================

    # ===================================== 部门管理  start  ===========================================
    get_department = '获取所有部门数据'
    add_department = '添加部门'
    update_department = '修改部门'
    delete_department = '删除部门'
    get_dpt_user_info_by_id = '获取部门下的员工数据'
    department_add_staff = '部门增加人员'
    delete_department_staff = '移除部门人员'
    # ===================================== 部门管理 end     ==========================================

    # ===================================== 角色权限管理 start   =======================================
    get_user_permission_info = '获取用户普通权限'
    get_data_permission_info = '获取用户数据权限'
    get_roles = '获取所有的角色数据'
    add_role = '添加角色'
    update_role = '修改角色'
    delete_role = '删除角色'
    add_role_permission = '给角色分配权限'
    get_role_permission_info = '获取角色的权限数据'
    # ===================================== 角色权限管理 end     =======================================


