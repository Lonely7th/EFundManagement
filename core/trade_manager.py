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


def fun_draw(data_list):
    plt.subplot(111)
    lable_x = np.arange(len(data_list))
    lable_y = [x * 0 for x in range(len(data_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, data_list, color="g", width=1.0)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(data_list) * 1.1, max(data_list) * 1.1)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # 获取数据
    db_manager_tk = DBManager("fcr_w_details")
    code_list = [x for x in db_manager_tk.get_code_list_02()]
    result_list = list()
    for item in code_list:
        tk_item = db_manager_tk.find_one_by_key({"ticker": item["ticker"]})
        # 计算成交量
        tk_details = tk_item["price_list"]
        close_list = [float(x["close"]) for x in tk_details if x["close"] != ""]
        open_list = [float(x["open"]) for x in tk_details if x["close"] != ""]
        high_list = [float(x["high"]) for x in tk_details if x["close"] != ""]
        low_list = [float(x["low"]) for x in tk_details if x["close"] != ""]
        volume_list = [float(x["volume"]) for x in tk_details if x["close"] != ""]
        for date in range(len(close_list)):
            close = close_list[date]
            open = open_list[date]
            high = high_list[date]
            low = low_list[date]

    if result_list:
        print(len(result_list))
        result_list_up = [x for x in result_list if x > 0]
        result_list_down = [x for x in result_list if x < 0]
        print(len(result_list_up), max(result_list_up), np.mean(result_list_up))
        print(len(result_list_down), min(result_list_down), np.mean(result_list_down))
    fun_draw(result_list)
