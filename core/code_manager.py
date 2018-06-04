#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/1'
"""
import random

from db.db_manager import DBManager


class CodeManager:
    def __init__(self):
        self.db_manager_tk = DBManager("tk_details")

    def get_buy_list(self, num=3):
        code_list = [x for x in self.db_manager_tk.get_code_list()]
        buy_list = list()
        for i in range(num):
            index = random.randint(0, len(code_list)-1)
            if code_list[index] not in buy_list:
                buy_list.append(code_list[index]["code"])
        return buy_list


if __name__ == "__main__":
    code_m = CodeManager()
    print(code_m.get_buy_list())
