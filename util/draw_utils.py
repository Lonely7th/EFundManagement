#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/1'
"""
import numpy as np
import matplotlib.pyplot as plt
import os


base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/bp/"


def draw_profit(path):
    file = open(base_path + path, "r")
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "cash->" in line:
            profit_list.append(round(float(line[6:]), 2))
    plt.subplot(211)
    lable_x = np.arange(len(profit_list))
    plt.plot(lable_x, profit_list, color="g", linewidth=1.0, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_list) * 0.9, max(profit_list) * 1.1)
    plt.grid(True)


def draw_w_profit_bar(path):
    file = open(base_path + path, "r")
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "cash->" in line:
            profit_list.append(round(float(line[6:]), 2))
    plt.subplot(212)
    profit_net_list = list()
    for index in range(1, len(profit_list)):
        profit_net_list.append((profit_list[index] - profit_list[index-1]) / profit_list[index-1])
    print(len([x for x in profit_net_list if x > 0]))
    print(len([x for x in profit_net_list if x < 0]))
    lable_x = np.arange(len(profit_net_list))
    lable_y = [x * 0 for x in range(len(profit_net_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, profit_net_list, color="r", width=0.8)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_net_list) * 1.1, max(profit_net_list) * 1.1)
    plt.grid(True)


def draw_manager(path):
    draw_profit(path)
    draw_w_profit_bar(path)
    plt.show()


if __name__ == "__main__":
    draw_manager("bp_result_fm_0.txt")
