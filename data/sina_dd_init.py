#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '获取大单数据'
__author__ = 'JN Zhang'
__mtime__ = '2018/6/14'
"""
import datetime

import tushare as ts


def date_range(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days + 1
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


if __name__ == "__main__":
    date_list = date_range("2018-01-01", "2018-12-31")
    for date in date_list:
        df = ts.get_sina_dd('000002', date=date)
        print(date, df)
    pass
