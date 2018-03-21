# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"
from lxml import html
import requests, re, json
from datetime import datetime

class Utils:

    # Чтение файла с названиями акций
    def read_tickers(self):
        with open('tickers.txt', mode='r') as f:
            line_list = []
            for line in f:
                line_list.append(line.rstrip())
            return line_list

    # Парсер
    def parser(self, page_dict):
        if page_dict['type'] == 'insider-trades':
            return(self.insider_trades(page_dict))
        elif page_dict['type'] == 'historical':
            return(self.historical(page_dict))
        else:
            print('error')

    # Генератор списка из url и сопутствующей информации
    def url_generator(self):
        all_company = self.read_tickers()
        for company in all_company:
            yield dict(company_name = company,
                       type = 'historical',
                       url = f'https://www.nasdaq.com/symbol/{company.lower()}/historical'
                       )

            for i in range(1,11):
                yield dict(company_name = company,
                           type = 'insider-trades',
                           url = f'https://www.nasdaq.com/symbol/{company.lower()}/insider-trades?page={i}'
                           )

    # Форматирование request Даты
    def format_data(self, date_value):
        # Если в ячейке даты лежит время заменяем его на текущую дату
        if len(date_value) < 10:
            return datetime.today().strftime('%Y-%m-%d')
        # Иначе форматируем данные
        else:
            date_list = date_value.split('/')
            return '{YYYY}-{MM}-{DD}'.format(YYYY=date_list[2], MM=date_list[0], DD=date_list[1])

    # Обработка historical request
    def historical(self, page_dict):

        # запрос структуры страницы
        page = requests.get(page_dict['url'])
        tree = html.fromstring(page.content)

        # выборка информации с помощью xpath
        page_table = tree.xpath(".//div[@id='quotes_content_left_pnlAJAX']/table/tbody/tr/td/text()")

        # Конкатенация полученных данных
        table_info = (''.join(page_table))

        # превидение данных к списку
        info_list = (re.findall(r'\s+(\S+)\s', re.sub('[,]', '', table_info)))
        info_dict = []

        while len(info_list):
            info_dict.append(dict(
                date=self.format_data(info_list[0]),
                open=info_list[1],
                high=info_list[2],
                low=info_list[3],
                close=info_list[4],
                volume=info_list[5]
            ))
            del info_list[:6]

        company_dict = dict(company=dict(short_name=page_dict['company_name'].lower()),
                            type='historical',
                            info=info_dict
                            )

        return json.dumps(company_dict, sort_keys=True, indent=4)

    # Обработка insider_trades request
    def insider_trades(self, page_dict):
        # запрос структуры страницы
        page = requests.get(page_dict['url'])
        tree = html.fromstring(page.content)

        # выборка информации с помощью xpath
        xpath_selection = list(tree.xpath(".//*[@class='genTable']/table/tr/td//text()"))
        info_dict = []
        while len(xpath_selection):
            if len(xpath_selection)<8 or xpath_selection[7].isupper():
                xpath_selection.insert(6,0)
            temp_list = xpath_selection[:8]
            del xpath_selection[:8]

            info_dict.append(dict(
                insider_name = temp_list[0],
                relation = temp_list[1],
                last_date = self.format_data(temp_list[2]),
                trans_type = temp_list[3],
                owner_type = temp_list[4],
                shares_traded = re.sub('[,]', '',temp_list[5]),
                last_price = temp_list[6],
                shares_held = re.sub('[,]', '',temp_list[7])
            ))
        company_dict = dict(company=dict(short_name=page_dict['company_name'].lower()),
                            type='insider-trades',
                            info=info_dict
                            )

        return json.dumps(company_dict, sort_keys=True, indent=4)


if __name__ == '__main__':
    i = Utils()

    pass
