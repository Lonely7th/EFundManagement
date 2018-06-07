#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/7'
"""
from db.db_manager import DBManager


class EmaManager:
    def __init__(self):
        self.db_manager_tk = DBManager("tk_details")

    def get_buy_list(self, date):
        code_list = [x for x in self.db_manager_tk.get_code_list_02()]
        buy_list = list()
        for itk_item in code_list:
            index = random.randint(0, len(code_list)-1)
            if code_list[index] not in buy_list:
                buy_list.append(code_list[index]["code"])
        return buy_list


if __name__ == "__main__":
    code_m = EmaManager()
    print(code_m.get_buy_list())
