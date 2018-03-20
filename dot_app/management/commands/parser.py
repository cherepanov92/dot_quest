# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.core.management.base import BaseCommand, CommandError
from dot_app.models import *
from dot_app.utils import Utils
import json
from datetime import datetime

from multiprocessing import Pool


class Command(BaseCommand):
    help = 'Парсинг'

    def __init__(self):
        super().__init__()
        self.stat = datetime.now()
        self.historical_col = 0
        self.insider_trades_col = 0

    def add_arguments(self, startparser):
        startparser.add_argument('multi_thread_col', nargs='+', type=int)

    def handle(self, *args, **options):
        for multi_thread_col in options['multi_thread_col']:
            parser = Utils()

            with Pool(multi_thread_col) as p:
                for json_request in (p.map(parser.parser, parser.url_generator())):
                    self.json_parser(json_request)

            stop = datetime.now()
            time = stop - self.stat

            print('за {time} минуты в {multi_thread_col}х канальном режиме было обработано:'.format(
                time = time,
                multi_thread_col = multi_thread_col))

            print('Создано {summ} записей:\n{historical_col} - historical и {insider_trades_col} - insider trades'\
                  .format(summ = self.historical_col + self.insider_trades_col,
                          historical_col = self.historical_col,
                          insider_trades_col = self.insider_trades_col
                          ))

    def company_in_DB(self, company):

        if Company.objects.filter(company_alias=company).exists():
            exist_company = Company.objects.get(company_alias=company)
            return exist_company.id
        else:
            new_company = Company(company_alias=company)
            new_company.save()
            return new_company.id

    def insider_in_db(self, insider):
        if Insider.objects.filter(name=insider['insider_name']).exists():
            exist_insider = Insider.objects.get(name=insider['insider_name'])
            return exist_insider.id
        else:
            new_insider = Insider(name=insider['insider_name'], relation=insider['relation'])
            new_insider.save()
            return new_insider.id

    def json_parser(self, json_data):

        data_json = json.loads(json_data)
        company_id = self.company_in_DB(data_json['company']['short_name'])
        if data_json['type'] == 'historical':
            for company_info in data_json['info']:
                Historical.objects.bulk_create([
                    Historical(
                        company_alias_id = company_id,
                        close = company_info['close'],
                        date = company_info['date'],
                        open = company_info['open'],
                        high = company_info['high'],
                        low = company_info['low'],
                        volume = company_info['volume']
                    )
                ])
                self.historical_col += 1
        elif data_json['type'] == 'insider-trades':
            for company_record in data_json['info']:
                insider_id = self.insider_in_db(company_record)
                InsiderTrades.objects.bulk_create([
                    InsiderTrades(
                        company_alias_id = company_id,
                        insider_id = insider_id,
                        last_date = company_record['last_date'],
                        trans_type = company_record['trans_type'],
                        owner_type = company_record['owner_type'],
                        shares_traded = company_record['shares_traded'],
                        last_price = company_record['last_price'],
                        shares_held = company_record['shares_held']
                    )
                ])
                self.insider_trades_col += 1
        else:
            raise ValueError()