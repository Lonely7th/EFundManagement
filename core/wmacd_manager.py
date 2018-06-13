#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/13'
"""
from db.db_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np


# 计算当前时间段的wmacd值
def get_w_macd(price_list):
    ema_12_list = list()
    for index in range(len(price_list)):
        if index == 0:
            ema_12_list.append(price_list[0])
        else:
            ema_12_list.append(round(ema_12_list[index - 1] * 11 / 13 + price_list[index] * 2 / 13, 4))
    ema_26_list = list()
    for index in range(len(price_list)):
        if index == 0:
            ema_26_list.append(price_list[0])
        else:
            ema_26_list.append(round(ema_26_list[index - 1] * 25 / 27 + price_list[index] * 2 / 27, 4))
    diff_list = list()
    for index in range(len(ema_12_list)):
        diff = ema_12_list[index] - ema_26_list[index]
        diff_list.append(diff)
    dea_list = list()
    for index in range(len(diff_list)):
        if index == 0:
            dea_list.append(diff_list[0])
        else:
            dea_list.append(round(dea_list[index - 1] * 0.8 + diff_list[index] * 0.2, 4))
    wmacd_list = list()
    for index in range(len(dea_list)):
        bar = (diff_list[index] - dea_list[index]) * 3
        wmacd_list.append(bar)
    return wmacd_list, diff_list, dea_list


if __name__ == "__main__":
    # 获取数据
    db_manager_tk = DBManager("fcr_w_details")
    code_list = [x for x in db_manager_tk.get_code_list_02()]
    k_list = list()
    for k in range(-10, 3):
        result_list = list()
        for item in code_list:
            tk_item = db_manager_tk.find_one_by_key({"ticker": item["ticker"]})
            # 计算成交量
            price_list = tk_item["price_list"]
            close_list = [float(x["close"]) for x in price_list if x["close"] != ""]
            volume_list = [float(x["volume"]) for x in price_list if x["close"] != ""]
            wmacd_list, diff_list, dea_list = get_w_macd(close_list)
            for date in range(len(close_list) - 1):
                if date > 26:
                    if wmacd_list[date] > 0 >= wmacd_list[date-1]:
                        if k > diff_list[date] > k-1:
                            if np.mean(volume_list[date-4:date-1]) < volume_list[date]:
                                profit_rate = (close_list[date + 1] - close_list[date]) / close_list[date]
                                result_list.append(profit_rate)
        if result_list:
            print(len(result_list))
            result_list_up = [x for x in result_list if x > 0]
            result_list_down = [x for x in result_list if x < 0]
            print(len(result_list_up), max(result_list_up), np.mean(result_list_up))
            print(len(result_list_down), min(result_list_down), np.mean(result_list_down))
            k_result = np.mean(result_list_up) + np.mean(result_list_down)
            print(k, k_result)
            k_list.append(k_result)
    # 绘图
    plt.subplot(111)
    lable_x = np.arange(len(k_list))
    lable_y = [x * 0 for x in range(len(k_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, k_list, color="g", width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(k_list) * 1.1, max(k_list) * 1.1)
    plt.grid(True)
    plt.show()
