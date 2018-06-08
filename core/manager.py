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
from core.ema_manager import EmaManager
from db.db_manager import DBManager
from util.date_utils import date_range, date_diff
from util.draw_utils import draw_manager

capital_base = 1000000  # 起始资金
current_position = list()  # 当前持仓
max_position = 5  # 最大持仓限制
history_capital = list()
history_order = list()
k_rate = 0.01  # 最低日均涨幅
d_rate = -0.03  # 最大跌幅(平仓线)


# 获取某个时间点的股票价格
def get_cur_values(code, date, key):
    result = [x[key] for x in db_manager_tk.find_by_key({'ticker': code})[0]["price_list"] if x["date"] == date]
    if result:
        return round(float(result[0]), 2)
    return 0


def get_position_by_code(code):
    for item in current_position:
        if item[0] == code:
            return item
    return []


# 计算当前资金总量
def get_all_capital():
    current_capital = capital_base
    for item_position in current_position[:]:
        current_capital += item_position[1] * item_position[2]
    return current_capital


# 买进股票
# position 仓位
def order_buy(code, date, amount, position):
    global capital_base
    open_price = get_cur_values(code, date, "open")
    if open_price != 0 and not np.isnan(open_price) and amount >= 100:
        if capital_base > open_price * amount:
            ticker = get_position_by_code(code)
            if ticker:  # 加仓
                surplus_value = ((ticker[1] * ticker[2]) + (open_price * amount)) / (ticker[2] + amount)
                ticker[1] = surplus_value  # 修改剩余价值
                ticker[2] = ticker[2] + amount  # 修改剩余持仓
                ticker[-1] = position
                ticker[-2] = date
                capital_base -= open_price * amount
                # 保存加仓记录
                bp_utils.insert_line("add-->" + json.dumps(ticker))
            else:  # 开仓
                if len(current_position) < max_position:
                    item_position = [code, open_price, amount, date, position]
                    current_position.append(item_position)
                    capital_base -= open_price * amount
                    # 保存开单记录
                    bp_utils.insert_line("buy-->" + json.dumps(item_position))


# 卖出股票
def order_sell(ticker, date, amount):
    global capital_base
    close_price = get_cur_values(ticker[0], date, "close")
    if ticker in current_position[:] and close_price != 0:
        if date_diff(ticker[-2], date) > 0:
            if amount < ticker[2]:  # 减仓
                surplus_value = ((ticker[1] * ticker[2]) - (close_price * amount)) / (ticker[2] - amount)
                ticker[1] = surplus_value  # 修改剩余价值
                ticker[2] = ticker[2] - amount  # 修改剩余持仓
                capital_base += close_price * amount
            else:  # 平仓
                profit_rate = (close_price - ticker[1]) * ticker[2] / get_all_capital()
                capital_base += close_price * ticker[2]
                bp_utils.insert_line("sell->" + json.dumps([ticker[0], str(round(profit_rate * 100, 2)) + "%", capital_base, date]))
                current_position.remove(ticker)


# 开仓逻辑
def fun_buy(buy_list, date):
    bp_utils.insert_line("date->" + date)
    p_stage = get_all_capital() / max_position  # 对资金池进行均分
    for code in buy_list:
        open_price = get_cur_values(code, date, "open")
        if open_price != 0 and not np.isnan(open_price):
            open_stage = p_stage / 10 * 2  # 当前资金段的2成开仓
            amount = int(open_stage / open_price / 100) * 100
            if amount >= 100:
                order_buy(code, date, amount, 1)


# 平仓逻辑
def fun_sell(date):
    for item_position in current_position[:]:
        close_price = get_cur_values(item_position[0], date, "close")
        if close_price != 0:
            profit_rate = (close_price - item_position[1]) / item_position[1]  # 总收益率
            if date_diff(item_position[-2], date) > 0 and profit_rate < d_rate and item_position in current_position:  # 跌破平仓线后
                order_sell(item_position, date, item_position[2])
            if date_diff(item_position[-2], date) > 0 and item_position in current_position:
                if close_price > item_position[1]:
                    expect_price = item_position[1] * ((1 + k_rate) ** date_diff(item_position[-2], date))  # 价格的期望值
                    if expect_price > close_price:
                        order_sell(item_position, date, item_position[2])
                    else:
                        if profit_rate > -d_rate and item_position[-1] < 5:
                            order_buy(item_position[0], date, item_position[2]/item_position[-1], item_position[-1]+1)
                else:
                    item_position[-2] = date
    # 统计历史数据
    history_capital.append(capital_base)
    bp_utils.insert_line("date->" + date)
    bp_utils.insert_line("cash->" + str(get_all_capital()))


def fun_buy_02(date, buy_list):
    p_stage = get_all_capital() / len(buy_list)  # 对资金池进行均分
    for code in buy_list:
        open_price = get_cur_values(code, date, "open")
        if open_price != 0 and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                order_buy(code, date, amount, 1)


def fun_sell_02(date, sell_list):
    for item_position in current_position[:]:
        if item_position[0] in sell_list:
            order_sell(item_position, date, item_position[2])


if __name__ == "__main__":
    code_ema = EmaManager()
    bp_utils = BPUtils("bp_result_fm_0.txt", "w")
    db_manager_tk = DBManager("fcr_details")
    # 初始化时间轴
    date_list = date_range("2017-01-01", "2017-12-31")
    for index in range(len(date_list)):
        cur_date = date_list[index]
        # 获取待购买的证券列表
        if datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 0:
            print(cur_date)
            buy_list = code_ema.get_buy_list(cur_date)
            print(cur_date, buy_list)
            if buy_list:
                fun_buy_02(cur_date, buy_list)
        if current_position and datetime.datetime.strptime(cur_date, "%Y-%m-%d").weekday() == 4:
            sell_list = code_ema.get_sell_list(cur_date)
            fun_sell_02(cur_date, sell_list)
    net_rate = (get_all_capital() - history_capital[0]) / history_capital[0]  # 计算回测结果
    # 统计交易结果
    print(round(net_rate * 100, 2), "%")
    # 绘图
    draw_manager("bp_result_fm_0.txt")
