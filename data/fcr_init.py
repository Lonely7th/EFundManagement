#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/5'
"""
import os

from db.db_manager import DBManager

base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/data/data_code.txt"

if __name__ == "__main__":
    # dm = DBManager("fcr_details")
    dm = DBManager("fcr_w_details")
    _file = open(base_path, "r", encoding="utf-8")
    tk_list = list()
    while True:
        line = _file.readline()
        if '' == line:
            break
        str_code = line.split()[0]
        str_title = line.split()[1]
        if "XSHE" in str_code:
            ticker = "sz." + str_code[:6]
        elif "XSHG" in str_code:
            ticker = "sh." + str_code[:6]
        dm.add_one({"code": str_code, "ticker": ticker, "title": str_title, "price_list": []})
