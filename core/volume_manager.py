#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/7'
"""
from db.db_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # 获取数据
    db_manager_tk = DBManager("fcr_details")
    code_list = [x for x in db_manager_tk.get_code_list_02()]
    for item in code_list:
        tk_item = db_manager_tk.find_one_by_key({"ticker": item["ticker"]})
        # 计算成交量
        price_list = tk_item["price_list"]
        for index in range(len(price_list)):
            tk_d_item = price_list[index]
            if index >= 20:
                tk_d_list = price_list[index-20: index]
                rsv_up = sum([int(x["volume"]) for x in tk_d_list if "-" not in x["pctChg"]]) / 20
                rsv_down = sum([int(x["volume"]) for x in tk_d_list if "-" in x["pctChg"]]) / 20
                if rsv_up + rsv_down != 0:
                    rsv = round(rsv_up / (rsv_up + rsv_down), 4)
                    tk_d_item["rsv"] = rsv
                else:
                    tk_d_item["rsv"] = 0
            else:
                tk_d_item["rsv"] = 0
        # K线图
        colse_list = [float(x["close"]) for x in price_list]
        plt.subplot(211)
        lable_x = np.arange(len(price_list))
        plt.plot(lable_x, colse_list, color="r", linewidth=1.0, linestyle="-")
        plt.xlim(lable_x.min(), lable_x.max() * 1.1)
        plt.ylim(min(colse_list) * 0.9, max(colse_list) * 1.1)
        plt.grid(True)
        # rsv图
        rsv_list = [x["rsv"] for x in price_list]
        plt.subplot(212)
        lable_x = np.arange(len(rsv_list))
        plt.plot(lable_x, rsv_list, color="g", linewidth=1.0, linestyle="-")
        plt.xlim(lable_x.min(), lable_x.max() * 1.1)
        plt.ylim(min(rsv_list) * 0.9, max(rsv_list) * 1.1)
        plt.grid(True)
        plt.show()
        # 数据分析
    pass
