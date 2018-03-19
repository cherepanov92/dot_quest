# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.core.management.base import BaseCommand, CommandError
from dot_app.models import *
from dot_app.utils import Utils
import json

from multiprocessing import Pool


class Command(BaseCommand):
    help = 'Парсинг'

    def company_in_DB(self, company):

        if Company.objects.filter(company_alias = company['short_name']).exists():
            exist_company = Company.objects.get(company_alias = company['short_name'])
            return exist_company.id
        else:
            new_company = Company(company_alias = company['short_name'])
            new_company.save()
            return new_company.id

    def insider_in_db(self, insider):
        if Insider.objects.filter(name = insider['insider_name']).exists():
            exist_insider = Insider.objects.get(name = insider['insider_name'])
            return exist_insider.id
        else:
            new_insider = Insider(name = insider['insider_name'], relation = insider['relation'])
            new_insider.save()
            return new_insider.id

    def add_arguments(self, parser):
        parser.add_argument('multi_thread_col', nargs='+', type=int)

    def handle(self, *args, **options):
            message = Utils()
            # data_json = json.loads(message.collect_insider_trades())
            # print(data_json)
            # for company_info in data_json:
            #     company_id = self.company_in_DB(company_info['company'])
            #     if company_info['type'] == 'historical':
            #         for one_record in company_info['info']:
            #             Historical.objects.bulk_create([
            #                 Historical(
            #                     company_alias_id = company_id,
            #                     close = one_record['close'],
            #                     date = one_record['date'],
            #                     open = one_record['open'],
            #                     high = one_record['high'],
            #                     low = one_record['low'],
            #                     volume = one_record['volume']
            #                 )
            #             ])
            #     elif company_info['type'] == 'insider_trades':
            #         print('===insider_trades===')
            #
            #         for company_record in company_info['info']:
            #             for one_record in company_record:
            #                 insider_id = self.insider_in_db(one_record)
            #                 print(insider_id, one_record['insider_name'], one_record['relation'], one_record['shares_held'])
            #
            #                 InsiderTrades.objects.bulk_create([
            #                     InsiderTrades(
            #                         company_alias_id = company_id,
            #                         insider_id = insider_id,
            #                         last_date = one_record['last_date'],
            #                         trans_type = one_record['trans_type'],
            #                         owner_type = one_record['owner_type'],
            #                         shares_traded = one_record['shares_traded'],
            #                         last_price = one_record['last_price'],
            #                         shares_held = one_record['shares_held']
            #                     )
            #                 ])
########################################################################################################################
            # for i in message.url_generator():
            #     print(i)

            with Pool(4) as p:
                p.map(message.parser, message.url_generator())

            # url =>| pool => html => info => json => DB
            '''
            чтение из файла
            для каждого лейбла делаем список
            name = goog
            создаём url на 3 мес
            добавляем к списку + тип historical
            создаём 10 записей добавляем к списку + тип InsiderTrades
            выгружаем
            '''