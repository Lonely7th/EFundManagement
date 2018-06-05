#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/5'
"""
import baostock as bs
import pandas as pd


if __name__ == "__main__":
    # 登陆系统
    lg = bs.login(user_id="anonymous", password="123456")
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取沪深A股历史K线数据
    # 详细指标参数，参见“历史行情指标参数”章节
    rs = bs.query_history_k_data("sh.600000",
                                 "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                 start_date='2017-07-01', end_date='2017-12-31',
                                 frequency="d", adjustflag="3")
    print('query_history_k_data respond error_code:' + rs.error_code)
    print('query_history_k_data respond  error_msg:' + rs.error_msg)

    #  打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    print(data_list)
    result = pd.DataFrame(data_list, columns=rs.fields)

    # print(result)

    # 登出系统
    bs.logout()
