#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: auth_helper.py
@create date: 2019-10-27 14:17 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
import json
import sys

import datetime
import jwt
import time
from flask import abort
from werkzeug.security import check_password_hash

import api
from db.user.db_user_mgr import user_mgr
from utils.status_code import response_code


class Auth(object):
    """
    权限校验、token帮助类
    """

    def __encode_auth_token(self, user_key, login_time):
        """
        生成认证Token
        :param USER_KEY: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            ##exp: 过期时间
            ##nbf: 表示当前时间在nbf里的时间之前，则Token不被接受
            ##iss: token签发者
            ##aud: 接收者
            ##iat: 发行时间
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'user_key': user_key,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                api.Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def __decode_auth_token(self, auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            ###十分钟无访问token过期
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, api.Config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'user_key' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'
        except TypeError:
            return '无效Token'
        except:
            print(sys.exc_info()[1])

    @classmethod
    def authenticate(cls, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        user = user_mgr.get_user_by_name(username)
        user_data = user.get('data')
        # 判断是有这个用户
        if (user_data is None):
            return response_code.LOGIN_IS_FAILD
        if user_data:
            # 验证密码
            if not check_password_hash(user_data.get('pass_word'), password):
                return response_code.LOGIN_IS_FAIL
            # 登录时间
            login_time = int(time.time())

            # 生成token
            token = cls._Auth__encode_auth_token(cls, user_data.get('id'), login_time)
            user_data.pop('pass_word')
            dict_user = user_data
            dict_user['token'] = token.decode()
            return dict_user
        else:
            return response_code.LOGIN_IS_FAILD

    @classmethod
    def identify(cls, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'Bearer' or len(auth_tokenArr) != 2):
                abort(401, 'Token错误或已过期，请重新登录')
            else:
                auth_token = auth_tokenArr[1]
                payload = cls.__decode_auth_token(cls, auth_token)
                if not isinstance(payload, str):
                    user_id = payload['data']['user_key']
                    userInfo = user_mgr.get_user_by_id(user_id)
                    if (userInfo is None):
                        abort(401, '找不到该用户信息')
                    else:
                        if True:
                            return payload['data']['user_key']
                        else:
                            abort(401, 'Token已更改，请重新登录获取')
                else:
                    abort(401, 'Token错误或已过期，请重新登录')
        else:
            abort(401, '没有提供认证token')
