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


base_path = os.path.abspath(os.path.join(os.getcwd(), "../..")) + "/bp/"


def draw_profit(file):
    profit_list = list()
    while True:
        line = file.readline()
        if "" == line:
            break
        if "cash->" in line:
            profit_list.append(round(float(line[6:]), 2))
    plt.subplot(111)
    lable_x = np.arange(len(profit_list))
    plt.plot(lable_x, profit_list, color="r", linewidth=1.0, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(profit_list) * 0.9, max(profit_list) * 1.1)
    plt.grid(True)
    plt.show()