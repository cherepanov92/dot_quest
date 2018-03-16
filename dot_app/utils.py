# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"
from lxml import html
import requests, re, json
from datetime import datetime

class Utils:

    # Чтение файла с названиями акций
    @staticmethod
    def read_tickers():
        with open('tickers.txt', mode='r') as f:
            line_list = []
            for line in f:
                line_list.append(line.rstrip())

            return line_list

    # Парсер

    def historical_parser(self, action):
        # запрос структуры страницы
        page = requests.get(f'https://www.nasdaq.com/symbol/{action}/historical')
        tree = html.fromstring(page.content)
        # выборка информации с помощью xpath
        full_action_name = tree.xpath(".//div[@id='qwidget_pageheader']/h1/text()")
        page_table = tree.xpath(".//div[@id='quotes_content_left_pnlAJAX']/table/tbody/tr/td/text()")
        # Конкатенация полученных данных
        table_info = (''.join(page_table))
        # превидение данных к списку
        info_list = (re.findall(r'\s+(\S+)\s', table_info))
        info_dict = []

        while len(info_list):
            # Если в ячейке даты лежит время заменяем его на текущую дату
            if len(info_list[0]) < 10:
                    info_list.pop(0)
                    info_list.insert(0, datetime.today().strftime('%Y-%m-%d'))
            else:
                # Форматирование даты
                info_date = info_list.pop(0).split('/')
                clear_data = '{YYYY}-{MM}-{DD}'.format(YYYY=info_date[2],MM=info_date[0],DD=info_date[1])
                info_list.insert(0, clear_data)

            # Форматирование суммы в число
            correct_volume = (info_list[5].replace(',',''))
            info_list.pop(5)
            info_list.insert(5, correct_volume)

            info_dict.append(list(info_list[:6]))
            del info_list[:6]
        action_dict = dict(action=dict(short_name = action, full_name = full_action_name),
                           info = info_dict)
        return action_dict

    def all_historical(self):
        all_historical = []

        # парсим страницы для всех акций из списка
        for action in Utils.read_tickers():
            all_historical.append(self.historical_parser(action))

        # Отдаём всю информацию JSON-ом
        return json.dumps(all_historical, sort_keys=True, indent=4)

if __name__ == '__main__':
    i = Utils()

    # print(i.read_tickers())


    # for info in i.parser():
    #     print(info)

    print(i.all_historical())

    pass