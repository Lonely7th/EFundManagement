#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JN Zhang'
__mtime__ = '2018/6/1'
"""
import os
base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/bp/"


class BPUtils:
    def __init__(self, file_name, _type):
        self.file = open(base_path + file_name, _type)

    def insert_line(self, line):
        if self.file:
            self.file.write(line + "\n")

    def raed_line(self):
        while True:
            line = self.file.readline()
            if '' == line:
                break
            yield line


if __name__ == "__main__":
    f_utils = BPUtils("test.txt", "a+")
    f_utils.insert_line("date:2018-04-24")
