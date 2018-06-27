#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据爬虫'
__author__ = 'JN Zhang'
__mtime__ = '2018/6/27'
"""
from time import sleep

from db.db_manager import DBManager
import baostock as bs


#### 获取沪深A股估值指标(日频)数据 ####
# peTTM    动态市盈率
# pbMRQ    市销率
# pcfNcfTTM    市现率
# pbMRQ    市净率


class HKDataCrawl:
    def __init__(self):
        self.dm = DBManager("fcr_details")

    def start_crawl(self):
        bs.login()
        code_list = self.dm.get_code_list_02()
        for item in code_list:
            ticker = item["ticker"]
            max_try = 8
            for tries in range(max_try):
                rs = bs.query_history_k_data(ticker, "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                                             start_date='2016-01-01', end_date='2017-12-31', frequency="d", adjustflag="2")
                if rs.error_code == '0':
                    self.parse_pager(rs, ticker)
                    break
                elif tries < (max_try - 1):
                    sleep(2)
                    continue
        bs.logout()

    def parse_pager(self, content, ticker):
        while content.next():
            item_row = content.get_row_data()
            __dict = {
                "date": item_row[0],
                "code": item_row[1],
                "close": item_row[2],
                "peTTM": item_row[3],
                "pbMRQ": item_row[4],
                "psTTM": item_row[5],
                "pcfNcfTTM": item_row[6]
            }
            self.dm.add_tk_item_k(ticker, __dict)
        print(ticker, "success")


if __name__ == '__main__':
    dc = HKDataCrawl()
    dc.start_crawl()
