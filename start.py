#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: start.py
@create date: 2019-10-27 10:20 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

import os

from api import create_app
from config import configuration

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    host, port, debug = configuration.get_start_config()
    app.run(host=host, port=port, debug=eval(debug))

