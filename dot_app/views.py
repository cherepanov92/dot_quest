import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
from .models import *

def index(request):
    if request.method == 'GET':
        all_company = Company.objects.all()
        context = {'title':'index', 'all_company': all_company}
        return render(request, 'dot_app/index.html', context)

def historical(request, ticker, api=False):
    ticker_obj = Company.objects.get(company_alias = ticker)
    ticker_historical = Historical.objects.filter(company_alias = ticker_obj)
    context = {'ticker': ticker, 'ticker_historical': ticker_historical,'date_from':'2018-01-11', 'date_to':'2018-01-08'}
    if api:
        context_api = serializers.serialize('json', ticker_historical)
        return HttpResponse(context_api, content_type='application/json')
    return render(request, 'dot_app/historical.html', context)

def insider(request, ticker, api=False):
    ticker_obj = Company.objects.get(company_alias=ticker)
    ticker_insider = InsiderTrades.objects.filter(company_alias=ticker_obj)
    context = {'ticker': ticker, 'ticker_insider': ticker_insider}
    if api:
        context_api = serializers.serialize('json', ticker_insider)
        return HttpResponse(context_api, content_type='application/json')
    return render(request, 'dot_app/insider.html', context)

def insider_name(request, ticker, insider_name, api=False):
    ticker_obj = Company.objects.get(company_alias=ticker)
    insider_obj = Insider.objects.get(name = insider_name)
    insider_data = InsiderTrades.objects.filter(company_alias=ticker_obj).filter(insider = insider_obj.id)
    context = {'ticker':ticker, 'insider_data':insider_data, 'insider_name':insider_name}

    if api:
        context_api = serializers.serialize('json', insider_data)
        return HttpResponse(context_api, content_type='application/json')

    return render(request, 'dot_app/insider_data.html', context)

def analytics(request, ticker, api=False):
    if request.method == 'GET':
        request_dict = request.GET
        if request_dict['date_from'] and request_dict['date_to']:
            ticker_obj = Company.objects.get(company_alias=ticker)
            date_from_obj = Historical.objects.filter(company_alias = ticker_obj).get(date = request_dict['date_from'])
            date_to_obj = Historical.objects.filter(company_alias = ticker_obj).get(date = request_dict['date_to'])
            decision = dict(open = round(date_to_obj.open - date_from_obj.open, 2),
                            high = round(date_to_obj.high - date_from_obj.high, 2),
                            low = round(date_to_obj.low - date_from_obj.low, 2),
                            close = round(date_to_obj.close - date_from_obj.close, 2),
                            volume = round(date_to_obj.volume - date_from_obj.volume, 2))


            context = {'ticker': ticker,
                       'date_from':date_from_obj,
                       'date_to':date_to_obj,
                       'decision':decision}
            if api:
                dump = json.dumps(decision)
                return HttpResponse(dump, content_type='application/json')

            return render(request, 'dot_app/analytics.html', context)

def delta(request, ticker, api=False):
    ticker_obj = Company.objects.get(company_alias=ticker)

    if request.method == 'GET':
        request_dict = request.GET
        if request_dict['value'] and request_dict['type'] in ['open','high','low','close']:

            s = (" SELECT MAX( select1.date ), date2 {up} FROM ("
                        " SELECT t1.date, t1.{type}, "
                        " MIN(t2.date) as date2 "
                        " FROM dot_app_historical t1 "
                        " INNER JOIN dot_app_historical t2 "
                        " ON (t2.{type} >= t1.{type} + {value} ) "
                        " AND t1.date < t2.date "
                        " AND t1.company_alias_id = t2.company_alias_id "
                        " WHERE t1.company_alias_id = {ticker_id} "
                        " GROUP BY t1.id "
                        " ORDER BY t1.date ) select1 "
                        " GROUP BY date2 "
                        " UNION "
                        " SELECT MAX( select2.date ), date2{down}FROM ( "
                        " SELECT t1.date, t1.{type}, "
                        " MIN(t2.date) as date2 "
                        " FROM dot_app_historical t1 "
                        " INNER JOIN dot_app_historical t2 "
                        " ON (t2.{type} <= t1.{type} - {value} ) "
                        " AND t1.date < t2.date "
                        " AND t1.company_alias_id = t2.company_alias_id "
                        " WHERE t1.company_alias_id = {ticker_id} "
                        " GROUP BY t1.id "
                        " ORDER BY t1.date ) select2 "
                        " GROUP BY date2 "
                        " ORDER BY date2; " .format(ticker_id = 1,
                                                    value = request_dict['value'],
                                                    type = request_dict['type'],
                                                    up = ", 'UP' direction ",
                                                    down = ", 'DOWN' as direction ")
                         )

            cursor = connection.cursor()
            cursor.execute(s)
            row = cursor.fetchall()
            context = {'ticker': ticker, 'row': row}

            return render(request, 'dot_app/delta.html', context)