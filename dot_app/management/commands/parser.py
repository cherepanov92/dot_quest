# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.core.management.base import BaseCommand, CommandError
from dot_app.models import *
from dot_app.utils import Utils


class Command(BaseCommand):
    help = 'Парсинг'

    def add_arguments(self, parser):
        parser.add_argument('multi_thread_col', nargs='+', type=int)

    def handle(self, *args, **options):
        for multi_thread_col in options['multi_thread_col']:

            message = Utils()
            data_list = message.parser()
            i = 0
            for data in  data_list:
                Historical.objects.bulk_create([
                    Historical(
                        company_alias_id = 1,
                        date = data[0],
                        open = data[1],
                        high = data[2],
                        low = data[3],
                        close = data[4],
                        volume = data[5],
                    )
                ])
                i += 1
            print(f'Записей добавлено: {i}')