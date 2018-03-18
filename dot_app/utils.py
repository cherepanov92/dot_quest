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

    # Парсинг компании
    def historical_parser(self, company):
        # запрос структуры страницы
        page = requests.get(f'https://www.nasdaq.com/symbol/{company}/historical')
        tree = html.fromstring(page.content)

        # выборка информации с помощью xpath
        full_company_name = tree.xpath(".//div[@id='qwidget_pageheader']/h1/text()")[0]
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

            info_dict.append(dict(
                        date = info_list[0],
                        open = info_list[1],
                        high = info_list[2],
                        low = info_list[3],
                        close = info_list[4],
                        volume = info_list[5]
                        ))
            del info_list[:6]
        company_dict = dict(
                            company=dict(short_name = company),
                            info = info_dict
                            )
        return company_dict

    # Объединение информации о нескольких компаниях
    def all_historical(self):
        all_historical = []

        # парсим страницы для всех акций из списка
        for company in Utils.read_tickers():
            all_historical.append(self.historical_parser(company))

        # Отдаём всю информацию JSON-ом
        return json.dumps(all_historical, sort_keys=True, indent=4)

    # Парсинг одной страницы insider_trades
    def insider_trades_parser(self, url):
        # запрос структуры страницы
        page = requests.get(url)
        tree = html.fromstring(page.content)

        # выборка информации с помощью xpath
        xpath_selection = list(tree.xpath(".//*[@class='genTable']/table/tr/td//text()"))
        info_list = []
        while len(xpath_selection):
            if len(xpath_selection)<8 or xpath_selection[7].isupper():
                xpath_selection.insert(6,0)
            temp_list = xpath_selection[:8]
            del xpath_selection[:8]

            # Форматирование даты
            info_date = temp_list.pop(2).split('/')
            clear_data = '{YYYY}-{MM}-{DD}'.format(YYYY=info_date[2], MM=info_date[0], DD=info_date[1])
            temp_list.insert(2, clear_data)

            info_list.append(dict(
                insider = temp_list[0],
                relation = temp_list[1],
                last_date = temp_list[2],
                trans_type = temp_list[3],
                owner_type = temp_list[4],
                shares_traded = temp_list[5],
                last_price = temp_list[6],
                shares_held = temp_list[7]
            ))
        return info_list

    # Объединение информации о всех страницах insider_trades
    def collect_insider_trades(self, company):
        all_insider_trades = []
        for i in range(1,10):
            url = f'https://www.nasdaq.com/symbol/{company}/insider-trades?page={i}'
            try:
                info = self.insider_trades_parser(url)
                '''
                Если дата последней страницы равна дате предпоследней страницы 
                это означает что прошлая страница была последней (информативной).
                Так-как сайт отдаёт страницу с последнем id даже если в id передаётся 
                значение больше самой старой страницы
                '''
                if all_insider_trades and info[-1]['last_date'] == all_insider_trades[-1][-1]['last_date']:
                    print('повтор инфориации')
                    break
                # print(info[-1]['last_date'])
                all_insider_trades.append(info)
            except Exception as error:
                print('ERROR', error)
        # print(all_insider_trades[-1][-1]['last_date'])
        return json.dumps(all_insider_trades, sort_keys=True, indent=4)

if __name__ == '__main__':
    i = Utils()
    i.collect_insider_trades('aapl')
    pass
