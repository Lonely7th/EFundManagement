#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据库管理类'
__author__ = 'JN Zhang'
__mtime__ = '2018/6/1'
"""
from pymongo import MongoClient


class DBManager:
    def __init__(self, table_name):
        # 指定端口和地址
        self.client = MongoClient("127.0.0.1", 27017)

        # 选择数据库
        self.db = self.client["tk_details"]
        self.table = self.db[table_name]

    def clsoe_db(self):
        self.client.close()

    def get_code_list(self):
        # 获取股票代码列表
        return self.table.find({}, {"code": 1}, no_cursor_timeout=True)

    def find_by_key(self, request={}):
        return self.table.find(request)
