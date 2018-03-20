from django.shortcuts import render
from .models import *

def index(request):
    if request.method == 'GET':
        all_company = Company.objects.all()
        context = {'title':'index', 'all_company': all_company}
        return render(request, 'dot_app/index.html', context)

def historical(request, ticker):
    ticker_obj = Company.objects.get(company_alias = ticker)
    ticker_historical = Historical.objects.filter(company_alias = ticker_obj)
    context = {'ticker': ticker, 'ticker_historical': ticker_historical,'date_from':'2018-01-11', 'date_to':'2018-01-08'}
    return render(request, 'dot_app/historical.html', context)

def insider(request, ticker):
    ticker_obj = Company.objects.get(company_alias=ticker)
    ticker_insider = InsiderTrades.objects.filter(company_alias=ticker_obj)
    context = {'ticker': ticker, 'ticker_insider': ticker_insider}
    return render(request, 'dot_app/insider.html', context)

def insider_name(request, ticker, insider_name):
    ticker_obj = Company.objects.get(company_alias=ticker)
    insider_obj = Insider.objects.get(name = insider_name)
    insider_data = InsiderTrades.objects.filter(company_alias=ticker_obj).filter(insider = insider_obj.id)
    context = {'ticker':ticker, 'insider_data':insider_data, 'insider_name':insider_name}
    return render(request, 'dot_app/insider_data.html', context)

def analytics(request, ticker):
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

            return render(request, 'dot_app/analytics.html', context)

