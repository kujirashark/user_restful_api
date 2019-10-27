#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: base.py
@create date: 2019-10-27 14:23 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：数据库操作基础类
"""


class DbBase(object):
    """ 数据库操作基础类"""

    def select_exec(self, conn, sql):
        """
        查询执行
        :param conn:
        :param sql:
        :return:
        """
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def updete_exec(self, conn, sql):
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def delete_exec(self, conn, sql):
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def insert_exec(self, conn, sql):
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def execute_sql_return_count(self, conn, sql, args=None):
        """
        增删改，返回受影响的行数
        :param sql: insert into tb_user(FuserName, Fpwd) values( % s, % s)
        :param args: tuple, list
        :return:
        """

        try:
            conn.cur.execute(sql, args)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def execute_many_data(self, conn, sql, data):
        """
        批量插入数据
        :param sql: 为insert语句
        :param data: 为list 格式为[[每一条数据],[]]
        :return:
        """
        try:
            conn.cur.executemany(sql, data)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def execute_many_sql_return_count(self, conn, sql, loop_args=None):
        """
        批量添加，返回受影响的行数
        :param sql: insert into tb_user(FuserName, Fpwd) values( % s, % s)
        :param args: loop(args)
        :return:
        """
        try:
            conn.cur.executemany(sql, loop_args)
            conn.conn.commit()
            return conn.cur.rowcount
        except Exception as ex:
            conn.conn.rollback()
            raise ex

    def execute_update_sql(self, conn, sql):
        """
        更新数据
        :param sql:
        :return:
        """
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
        except:
            conn.conn.rollback()

    def execute_del_data(self, conn, sql):
        """
        删除数据
        :param conn:
        :param sql:
        :return:
        """
        try:
            conn.cur.execute(sql)
            conn.conn.commit()
        except Exception as e:
            conn.conn.rollback()

    def execute_fetch_one(self, conn, sql, args=None):
        """循环执行查询语句，返回查询数据
        :param sql: select user,pass from tb7 where user=%s and pass=%s
        :param loop_args: tuple, list
        :return: dict
        """
        try:
            conn.cur.execute(sql, args)
            result = conn.cur.fetchone()
            if result:
                return result
                # return dict(result)
            else:
                return {}
        except Exception as ex:
            raise ex

    def execute_fetch_all(self, conn, sql, args=None):
        """循环执行查询语句，返回查询数据
        :param sql: select user,pass from tb7 where user=%s and pass=%s
        :param loop_args: tuple, list 4444
        :return: list[dict]
        """
        # 请使用db_session连接数据库
        try:
            conn.cur.execute(sql, args)
            result = conn.cur.fetchall()
            if result:
                return result
            else:
                return []
        except Exception as ex:
            raise ex

    def excuteLoopFetchAll(self, conn, keys, loop_sql, loop_args):
        """循环执行查询语句，更具keys返回查询集合
        :param keys: tuple, list
        :param sql: loop(select user,pass from tb7 where user=%s and pass=%s)
        :param loop_args: 二维数组
        :return: dict[list[dict]]
        """
        try:
            result = {}
            for key, sql, args in zip(keys, loop_sql, loop_args):
                if args:
                    count = conn.cur.execute(sql, args)
                    if count > 0:
                        data = conn.cur.fetchall()
                        result[key] = [dict(x) for x in data]
                else:
                    result[key] = []
            return result
        except Exception as ex:
            raise ex

    def execute_fetch_pages(self, conn, sql_count, sql, page_index, page_size, args=None):
        """
        分页查询语句
        :param conn:
        :param sql_count:
        :param sql:
        :param page_index:
        :param page_size:
        :param args:
        :return:
        """
        try:
            conn.cur.execute(sql_count, args)
            total_count = conn.cur.fetchone().get('count(*)')
            conn.cur.execute(sql, args)
            result_data = conn.cur.fetchall()
            if len(result_data) == 0:
                result_data = []
            page_list_json = {"page_size": page_size, "page_index": page_index, "total_count": total_count,
                              "total_page": 1, "data_list": result_data}
            if total_count % page_size == 0:
                total_page = total_count / page_size
            else:
                total_page = math.ceil(total_count / page_size)
            page_list_json["total_page"] = total_page
            return page_list_json
        except Exception as ex:
            raise ex

    def create_insert_sql(self, db_name, table_name, fields, tuple):
        """
        插入语句sql组装
        :param fields: 要插入的字段
        :param tuple: 要插入的数据
        :param table_name: 被插入的表的名称
        :param db_name: 被插入数据的数据库名称
        :return:
        """
        sql = 'insert into %s.%s %s values %s' % (db_name, table_name, fields, tuple)

        return sql

    def create_update_sql(self, db_name, table_name, fields, tuple, condition):
        """
        修改数据的sql
        :param db_name:  数据库名称
        :param table_name:  数据表名称
        :param fields: 需要修改的字段列表
        :param tuple:  需要修改字段对应的值
        :param condition: 以什么条件去修改
        :return:
        """
        sql = "update %s.%s set " % (db_name, table_name)
        for index, filed in enumerate(fields):
            if filed != fields[-1]:
                if isinstance(tuple[index], str):
                    sql += filed + "=" + "'" + str(tuple[index]) + "'" + ","
                else:
                    sql += filed + "=" + str(tuple[index]) + ","
            else:
                if isinstance(tuple[index], str):
                    sql += filed + "=" + "'" + str(tuple[index]) + "'" + " "
                else:
                    sql += filed + "=" + str(tuple[index]) + " "
        sql += "where " + condition
        return sql

    def create_delete_sql(self, db_name, table_name, condition):
        """
        删除数据的sql
        :param db_name:
        :param table_name:
        :param condition:
        :return:
        """
        sql = "delete from %s.%s where %s" % (db_name, table_name, condition)
        return sql

    def create_get_page_sql(self, db_name, table_name, fields, start_page, page_size, condition=None):
        """
        分页sql语句
        :param db_name:
        :param table_name:
        :param fields:
        :param start_page:
        :param page_size:
        :param condition:
        :return: 查询sql和计数sql
        """
        sql_count = "select count(*) from %s.%s" % (db_name, table_name)
        sql = "select %s from %s.%s" % (fields, db_name, table_name)
        if (condition == None) or (condition == "") or (condition == " "):
            sql += " limit %s,%s" % (start_page, page_size)
            sql_count = sql_count
        else:
            sql += " where " + condition + " limit %s,%s" % (start_page, page_size)
            sql_count += " where " + condition

        # print(sql_count)
        # print(sql)
        return sql_count, sql

    def create_select_sql(self, db_name, table_name, fields, condition=None):
        """
        获取某个字段的查询语句
        :param db_name:
        :param table_name:
        :param fields:
        :param condition:
        :return: sql
        """

        sql = "select %s from %s.%s" % (fields, db_name, table_name)
        if condition == None:
            sql = sql
        else:
            sql += " where " + condition
        return sql

    def create_get_relation_sql(self, db_name=None, table_name=None, fields=None, relations=None, condition=None):
        """
        创建关联查询sql语句
        :param db_name:
        :param table_name:
        :param fields:
        :param relations:
        :param condition:
        :return:
        """
        if db_name:
            sql = "select %s from %s.%s" % (fields, db_name, table_name)
            if relations:
                for relation in relations:
                    sql += " left join " + db_name + "." + relation["table_name"] + " on " + relation["join_condition"]
            if condition is None:
                sql = sql
            else:
                sql += " where " + condition
        else:
            sql = "select %s from %s" % (fields, table_name)
            if relations:
                for relation in relations:
                    sql += " left join " + relation["table_name"] + " on " + relation["join_condition"]
            if condition is None:
                sql = sql
            else:
                sql += " where " + condition

        return sql

    def create_get_relation_page_sql(self, db_name, table_name, fields, relations, start_num, page_size,
                                     condition=None):
        """
        分页,多表关联查询sql语句
        :param db_name:
        :param table_name:
        :param fields:
        :param relations：关联关系
        :param start_page:
        :param page_size:
        :param condition:
        :return: 查询sql和计数sql
        """
        sql_count = "select count(*) from %s.%s" % (db_name, table_name)
        sql = "select %s from %s.%s" % (fields, db_name, table_name)
        if relations:
            for relation in relations:
                sql += " left join " + db_name + "." + relation["table_name"] + " on " + relation["join_condition"]
        if condition == None:
            sql += " limit %s,%s" % (start_num, page_size)

            sql_count = sql_count
        else:
            sql += " where " + condition + " limit %s,%s" % (start_num, page_size)
            sql_count += " where " + condition

        return sql_count, sql

    def create_batch_insert_sql(self, db_name, table_name, insert_data_list):
        """
        生成批量插入数据的sql
        :param db_name:
        :param table_name:
        :param insert_data_list:
        :return: sql和对应的插入数据
            例如:
                sql: 'insert into db_name.table_name (c_id,c_no) values (%s,%s)'
                数据: [[1, 2], [2, 3]]
        """
        insert_data = []
        sql = """insert into %s.%s (""" % (db_name, table_name)
        if insert_data_list:
            for s in insert_data_list:
                insert_data.append(list(s.values()))

            fields = list(insert_data_list[0].keys())
            index = 0
            # 添加 sql 前面的的字段
            for i in fields:
                if index == len(fields) - 1:
                    sql += '%s' % i
                else:
                    sql += '%s,' % i
                index += 1
            sql += ') values ('
            # 添加sql values后面的字段
            flag = 0
            for _ in fields:
                if flag == len(fields) - 1:
                    sql += '%s'
                else:
                    sql += '%s,'
                flag += 1

            sql += ')'
        else:
            sql += ')'
            insert_data = []

        return sql, insert_data

    def create_vague_condition_sql(self, search_data):
        """
        生成模糊查询搜索条件
        :param search_data:
        例如:
            search_data = {'c_name':2,'c_no':2}
            search_data = json.dumps(search_data)
        :return: 组合好的条件
            例如: cmd_name like '%2%' and cmd_no like '%2%'
        """
        search_data_dict = json.loads(search_data)
        index = 0
        condition = ' '
        if len(search_data_dict) == 0:
            return ""
        for k, v in search_data_dict.items():
            if index == len(search_data_dict) - 1:
                condition += str(k) + " like '%" + str(v) + "%'"
            else:
                condition += str(k) + " like '%" + str(v) + "%'" + " and "
            index += 1
        return condition

    def insert_sql(self, db_name, table_name, data_dict):
        """
        创建插入语句
        :param db_name: 数据库名
        :param table_name: 表名
        :param json_object: 字典数据
        :return: sql
        """
        insert_data = []
        fields = "("
        flag = 1
        for key, value in data_dict.items():
            if flag == len(data_dict):
                fields += key
            else:
                fields += key + ","
            insert_data.append(value)
            flag += 1
        fields += ")"
        if len(insert_data) == 1:
            insert_data = str(tuple(insert_data))
            insert_data = insert_data.replace(',', '')
        else:
            insert_data = str(tuple(insert_data))
        sql = 'insert into %s.%s %s values %s' % (db_name, table_name, fields, insert_data)

        return sql

    def update_sql(self, db_name, table_name, data_dict, condition):
        """
        修改数据的sql
        :param db_name:  数据库名称
        :param table_name:  数据表名称
        :param json_object: 字典数据
        :param condition: 以什么条件去修改
                例如: 'S_KEY=6 and S_NO = 1001'
        :return: sql
        """
        sql = "update %s.%s set " % (db_name, table_name)
        flag = 1
        for key, value in data_dict.items():
            if flag == len(data_dict):
                if isinstance(value, str):
                    sql += key + " = " + "'" + value + "'"
                else:
                    sql += key + " = " + str(value)
            else:
                if isinstance(value, str):
                    sql += key + " = " + "'" + value + "'" + ","
                else:
                    sql += key + " = " + str(value) + ","
            flag += 1

        sql += " where " + condition

        return sql
