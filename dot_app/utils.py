# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

# Чтение файла с названиями акций
def read_tickers():
    with open(r'../tickers.txt', mode='r') as f:
        line_list = []
        for line in f:
            line_list.append(line.rstrip())

        return line_list

if __name__ == '__main__':
    print(read_tickers())

