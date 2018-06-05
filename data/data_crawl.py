#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据爬虫'
__author__ = 'JN Zhang'
__mtime__ = '2018/6/5'
"""
from time import sleep

from db.db_manager import DBManager
import baostock as bs
'''
参数名称	参数描述
date	交易所行情日期
code	证券代码
open	开盘价
high	最高价
low	最低价
close	收盘价
preclose	昨日收盘价
volume	成交量（累计 单位：股）
amount	成交额（单位：人民币元）
adjustflag	复权状态(1：后复权， 2：前复权，3：不复权）
turn	换手率
tradestatus	交易状态(1：正常交易 0：停牌）
pctChg	涨跌幅
peTTM	动态市盈率
pbMRQ	市净率
psTTM	市销率
pcfNcfTTM	市现率
isST	是否ST股，1是，0否
'''


class ENDataCrawl:
    def __init__(self):
        self.dm = DBManager("fcr_details")

    def start_crawl(self):
        bs.login(user_id="anonymous", password="123456")
        code_list = self.dm.get_code_list_02()
        for item in code_list:
            ticker = item["ticker"]
            max_try = 8
            for tries in range(max_try):
                rs = bs.query_history_k_data(ticker, "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg",
                                             start_date='2016-01-01', end_date='2017-12-31', frequency="d", adjustflag="2")
                if rs.error_code == '0':
                    self.parse_pager(rs, ticker)
                    break
                elif tries < (max_try - 1):
                    sleep(2)
                    continue
        bs.logout()

    def parse_pager(self, content, ticker):
        timer_list = [x["date"] for x in self.dm.find_one_by_key({"ticker": ticker})["price_list"]]
        while content.next():
            item_row = content.get_row_data()
            __dict = {
                "date": item_row[0],
                "code": item_row[1],
                "open": item_row[2],
                "high": item_row[3],
                "low": item_row[4],
                "close": item_row[5],
                "preclose": item_row[6],
                "volume": item_row[7],
                "amount": item_row[8],
                "adjustflag": item_row[9],
                "turn": item_row[10],
                "tradestatus": item_row[11],
                "pctChg": item_row[12]
            }
            if __dict["date"] not in timer_list:
                self.dm.add_tk_item(ticker, __dict)
        print(ticker, "success")


if __name__ == '__main__':
    dc = ENDataCrawl()
    dc.start_crawl()
