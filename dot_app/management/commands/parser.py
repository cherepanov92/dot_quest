# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.core.management.base import BaseCommand, CommandError
from dot_app.models import *
from dot_app.utils import Utils
import json


class Command(BaseCommand):
    help = 'Парсинг'

    def company_in_DB(self, company):

        if Company.objects.filter(company_alias = company['short_name']).exists():
            exist_company = Company.objects.get(company_alias = company['short_name'])
            print('Компания {} уже существует'.format(company['short_name']))
            return exist_company.id
        else:
            new_company = Company(company_alias = company['short_name'], company_name = company['full_name'])
            new_company.save()
            print('Добавлена компания {}'.format(company['short_name']))
            return new_company.id

    def add_arguments(self, parser):
        parser.add_argument('multi_thread_col', nargs='+', type=int)

    def handle(self, *args, **options):
        # for multi_thread_col in options['multi_thread_col']:

            message = Utils()
            data_json = json.loads(message.all_historical())
            i = 0
            for company_info in data_json:
                company_id = self.company_in_DB(company_info['company'])

                for one_record in company_info['info']:
                    Historical.objects.bulk_create([
                        Historical(
                            company_alias_id = company_id,
                            close = one_record['close'],
                            date = one_record['date'],
                            open = one_record['open'],
                            high = one_record['high'],
                            low = one_record['low'],
                            volume = one_record['volume']
                        )
                    ])
                    i += 1
                    print(f'Запись {i} добавлена')

                print(f'Записей добавлено: {i}')