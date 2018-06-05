#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '策略管理'
__author__ = 'JN Zhang'
__mtime__ = '2018/06/01'
"""
import datetime
import json
import numpy as np

from bp.bp_utils import BPUtils
from core.code_manager import CodeManager
from db.db_manager import DBManager
from util.draw_utils import draw_manager

capital_base = 1000000  # 起始资金
current_position = list()  # 当前持仓
max_position = 5  # 最大持仓限制
history_capital = list()
history_order = list()
k_rate = 0.01  # 最低日均涨幅
d_rate = -0.05  # 最大跌幅(平仓线)


# 时间轴
def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


# 时间差
def date_diff(start, end, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return int(days)


# 获取某个时间点的股票价格
def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'code': code})[0]["price_list"] if x["date"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


# 计算当前资金总量
def get_all_capital():
    current_capital = capital_base
    for item_position in current_position[:]:
        current_capital += item_position[1] * item_position[2]
    return current_capital


# 开仓
def fun_buy(buy_list, date):
    global capital_base
    bp_utils.insert_line("date->" + date)
    p_stage = get_all_capital() / max_position  # 对资金池进行均分
    for code in buy_list:
        if len(current_position) < max_position:
            open_price = get_cur_values(code, date, "open")
            if open_price != 0 and not np.isnan(open_price):
                open_stage = p_stage / 10 * 4  # 当前资金段的4成开仓
                amount = int(open_stage / open_price / 100) * 100
                if amount >= 100:
                    item_position = [code, open_price, amount, date, 0]
                    current_position.append(item_position)
                    capital_base -= open_price * amount
                    # 保存开单记录
                    bp_utils.insert_line("buy-->" + json.dumps(item_position))


# 加仓
def fun_add():
    pass


# 平仓
def fun_sell(date):
    global capital_base
    for item_position in current_position[:]:
        close_price = get_cur_values(item_position[0], date, "close")
        if close_price != 0:
            profit_rate = (close_price - item_position[1]) / item_position[1]  # 总收益率
            if date_diff(item_position[-1], date) > 0 and profit_rate < d_rate and item_position in current_position:  # 跌破平仓线后
                bp_utils.insert_line("date->" + date)
                capital_base += close_price * item_position[2]
                bp_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                current_position.remove(item_position)
            if date_diff(item_position[-1], date) > 5 and item_position in current_position:
                expect_price = item_position[1] * ((1 + k_rate)**date_diff(item_position[-1], date))  # 价格的期望值
                # expect_price = item_position[1] * (1 + (k_rate * date_diff(item_position[-1], date)))  # 价格的期望值
                if close_price >= item_position[1]:
                    if expect_price > close_price:
                        bp_utils.insert_line("date->" + date)
                        capital_base += close_price * item_position[2]
                        bp_utils.insert_line("sell->" + json.dumps([item_position[0], str(round(profit_rate * 100, 2)) + "%", capital_base]))
                        current_position.remove(item_position)
                    # else:
                        # 如果满足涨幅条件则加仓
                else:
                    item_position[-1] = date
    # 统计历史数据
    history_capital.append(capital_base)
    bp_utils.insert_line("cash->" + str(get_all_capital()))


if __name__ == "__main__":
    code_m = CodeManager()
    bp_utils = BPUtils("bp_result_fm_0.txt", "w")
    db_manager_tk = DBManager("fcr_details")
    # 初始化时间轴
    date_list = date_range("2017-01-01", "2017-12-31")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        # 获取待购买的证券列表
        buy_list = code_m.get_buy_list()
        print(cur_date, buy_list)
        if buy_list:
            fun_buy(buy_list, cur_date)
        # 管理仓位
        fun_sell(cur_date)
    net_rate = (get_all_capital() - history_capital[0]) / history_capital[0]  # 计算回测结果
    # 统计交易结果
    print(round(net_rate * 100, 2), "%")
    # 绘图
    draw_manager("bp_result_fm_0.txt")
