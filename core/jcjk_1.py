#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/27'
"""
from db.db_manager import DBManager
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    db_manager_tk = DBManager("fcr_details")
    code_list = [x for x in db_manager_tk.get_code_list_02()]
    pe_list = list()
    for item in code_list:
        tk_item = db_manager_tk.find_one_by_key({"ticker": item["ticker"]})
        tk_code = tk_item["ticker"]
        if "hk_list" in str(tk_item):
            hk_list = [float(x["peTTM"]) for x in tk_item["hk_list"]][250:]
            colse_list = [float(x["close"]) for x in tk_item["price_list"]][250:]
            if len(hk_list) > 0 and 17 < hk_list[0] < 21:
                v = (colse_list[-1] - colse_list[0]) / colse_list[0]
                print(colse_list[0], colse_list[-1], tk_code, v)
                pe_list.append(v)
                plt.subplot(211)
                lable_x = np.arange(len(colse_list))
                plt.plot(lable_x, colse_list, color="r", linewidth=1.0, linestyle="-")
                plt.xlim(lable_x.min(), lable_x.max() * 1.1)
                plt.ylim(min(colse_list) * 0.9, max(colse_list) * 1.1)
                plt.grid(True)
                plt.subplot(212)
                lable_x = np.arange(len(hk_list))
                plt.plot(lable_x, hk_list, color="r", linewidth=1.0, linestyle="-")
                plt.xlim(lable_x.min(), lable_x.max() * 1.1)
                plt.ylim(min(hk_list) * 0.9, max(hk_list) * 1.1)
                plt.grid(True)
                plt.title(tk_code)
                plt.show()
    print("len", len(pe_list), "up", len([x for x in pe_list if x > 0]), "down", len([x for x in pe_list if x < 0]),
          "mean", np.mean(pe_list), "max", np.max(pe_list), "min", np.min(pe_list))
    # print("up", len([x for x in pe_list if x > 0]))
    # print("down", len([x for x in pe_list if x < 0]))
    # print("mean", np.mean(pe_list))
    # print("max", np.max(pe_list))
    # print("min", np.min(pe_list))
    # pe_stage = list()
    # for step in range(0, 300, 10):
    #     start = step
    #     end = step + 10
    #     pe_stage.append(len([x for x in pe_list if start < x < end]))
    # plt.subplot(111)
    # lable_x = np.arange(len(pe_stage))
    # lable_y = [x * 0 for x in range(len(pe_stage))]
    # # 绘制中轴线
    # plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    # plt.bar(lable_x, pe_stage, color="g", width=1.0)
    # plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    # plt.ylim(min(pe_stage) * 1.1, max(pe_stage) * 1.1)
    # plt.grid(True)
    # plt.show()
