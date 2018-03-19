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

    def add_arguments(self, parser):
        parser.add_argument('multi_thread_col', nargs='+', type=int)

    def handle(self, *args, **options):
            parser = Utils()

            with Pool(10) as p:
                for json_request in (p.map(parser.parser, parser.url_generator())):
                    self.json_parser(json_request)

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
        print(data_json, '\n')

        company_id = self.company_in_DB(data_json['company']['short_name'])
        if data_json['type'] == 'historical':
            for company_info in data_json['info']:
                print(company_info)
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
                # print('{type}{company_name} append'.format(type = company_info['type'], company_name = company_info['company']))
        # elif data_json['type'] == 'insider-trades':
        #     print('===insider_trades===')
        #     for company_record in data_json['info']:
        #         print(company_record)


                # for one_record in company_record:

                    # insider_id = self.insider_in_db(one_record)
                    # print(insider_id, one_record['insider_name'], one_record['relation'], one_record['shares_held'])
                    #
                    # InsiderTrades.objects.bulk_create([
                    #     InsiderTrades(
                    #         company_alias_id = company_id,
                    #         insider_id = insider_id,
                    #         last_date = one_record['last_date'],
                    #         trans_type = one_record['trans_type'],
                    #         owner_type = one_record['owner_type'],
                    #         shares_traded = one_record['shares_traded'],
                    #         last_price = one_record['last_price'],
                    #         shares_held = one_record['shares_held']
                    #     )
                    # ])
#
#
#
#
#
#
# # if __name__ == '__main__':
# #     i = Command()
# #     i.pool()
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