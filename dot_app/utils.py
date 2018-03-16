# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

class Utils:

    # Чтение файла с названиями акций
    @staticmethod
    def read_tickers():
        with open(r'../tickers.txt', mode='r') as f:
            line_list = []
            for line in f:
                line_list.append(line.rstrip())

            return line_list

    # Парсер

    def parser(self):
        from lxml import html
        import requests
        import re
        from datetime import datetime
        # запрос структуры страницы
        page = requests.get('https://www.nasdaq.com/symbol/cvx/historical')
        tree = html.fromstring(page.content)
        # выборка информации с помощью xpath
        page_table = tree.xpath(".//div[@id='quotes_content_left_pnlAJAX']/table/tbody/tr/td/text()")
        # Конкатенация полученных данных
        table_info = (''.join(page_table))
        # превидение данных к списку
        info_list = (re.findall(r'\s+(\S+)\s', table_info))
        info_dict = []

        while len(info_list):
            # Если в ячейке даты лежит время заменяем его на текущую дату
            if not re.match(r'\d{2}\/\d{2}\/\d{4}',info_list[0]):
                    info_list.pop(0)
                    info_list.insert(0, datetime.today().strftime('%Y-%m-%d'))
            # Форматирование суммы в число
            correct_volume = (info_list[5].replace(',',''))
            info_list.pop(5)
            info_list.insert(5, correct_volume)

            info_dict.append(list(info_list[:6]))
            del info_list[:6]

        return info_dict



if __name__ == '__main__':
    i = Utils()

    # print(i.read_tickers())


    for info in i.parser():
        print(info)

    pass