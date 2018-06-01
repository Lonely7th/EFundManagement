#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '启动服务'
__author__ = 'JN Zhang'
__mtime__ = '2018/06/01'
"""
import datetime
import json
import numpy as np

from bp.bp_utils import BPUtils
from core.code_manager import CodeManager
from db.db_manager import DBManager

capital_base = 1000000
capital_available = capital_base
current_position = list()
history_capital = list()
history_order = list()
k_rate = 0.05
d_rate = -0.03


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["cur_timer"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


def fun_buy(buy_list, date):
    global capital_base
    bp_utils.insert_line("date->" + date)
    p_stage = capital_base / len(buy_list)  # 对资金池进行均分
    for code in buy_list:
        open_price = get_cur_values(code, date, "cur_open_price")
        if open_price != 0 and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                item_position = [code, open_price, amount, date]
                current_position.append(item_position)
                capital_base -= open_price * amount
                # 保存开单记录
                bp_utils.insert_line("buy-->" + json.dumps(item_position))


def fun_sell(date):
    global capital_base
    if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 4:
        bp_utils.insert_line("date->" + date)
        for item_position in current_position[:]:
            close_price = get_cur_values(item_position[0], date, "cur_close_price")
            if close_price != 0:
                profit_rate = (close_price - item_position[1]) / item_position[1]  # 计算收益率
                capital_base += close_price * item_position[2]
                bp_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                current_position.remove(item_position)
        # 统计历史数据
        history_capital.append(capital_base)
        bp_utils.insert_line("cash->" + str(capital_base))


if __name__ == "__main__":
    code_m = CodeManager()
    bp_utils = BPUtils("bp_result3_1.txt", "a+")
    db_manager_tk = DBManager("tk_details")
    # 初始化时间轴
    date_list = date_range("2016-06-05", "2018-03-09")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            # 获取待购买的证券列表
            buy_list = code_m.get_buy_list()
            if buy_list:
                fun_buy(buy_list, cur_date)
        else:
            fun_sell(cur_date)
    net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
    # 统计交易结果
    print(round(net_rate * 100, 2), "%")
    pass