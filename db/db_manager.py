#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据库管理类'
__author__ = 'JN Zhang'
__mtime__ = '2018/6/1'
"""
import datetime

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

    def get_code_list_02(self):
        # 获取股票代码列表(sz格式)
        return self.table.find({}, {"ticker": 1}, no_cursor_timeout=True)

    def find_by_key(self, request={}):
        return self.table.find(request)

    def find_one_by_key(self, request={}):
        return self.table.find_one(request)

    def add_one(self, post, created_time=datetime.datetime.now()):
        # 添加一条数据
        post['created_time'] = created_time
        return self.table.insert_one(post)

    def add_tk_item(self, ticker, __dict):
        return self.table.update_one({'ticker': ticker}, {"$push": {"price_list": __dict}})

    def add_tk_item_k(self, ticker, __dict):
        return self.table.update_one({'ticker': ticker}, {"$push": {"hk_list": __dict}})
