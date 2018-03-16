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
            try:
                message = Utils()
                print(message.parser())
                # Historical.objects.all()
            except Exception:
                print('bad')