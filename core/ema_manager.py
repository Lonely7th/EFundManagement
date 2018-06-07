#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/7'
"""
import datetime
import numpy as np

from db.db_manager import DBManager


def time_cmp(first_time, second_time):
    return datetime.datetime.strptime(first_time, "%Y-%m-%d") >= datetime.datetime.strptime(second_time, "%Y-%m-%d")


class EmaManager:
    def __init__(self):
        self.db_manager_tk = DBManager("fcr_w_details")

    def get_buy_list(self, date):
        code_list = [x for x in self.db_manager_tk.get_code_list_02()]
        buy_list = list()
        for code_item in code_list:
            ticker = code_item["ticker"]
            # 获取数据
            close_list = list()
            tk_details = self.db_manager_tk.find_one_by_key({"ticker": ticker})
            for tk_item in [x for x in tk_details["price_list"]]:
                if time_cmp(str(date), tk_item["date"]):
                    close_list.append(tk_item["close"])
            # 执行判断条件
            ema_20 = np.mean(close_list[-20:])
        return buy_list

    def get_sell_list(self, date):
        pass


if __name__ == "__main__":
    code_m = EmaManager()
    print(code_m.get_buy_list())
