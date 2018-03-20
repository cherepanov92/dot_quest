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
    context = {'ticker': ticker, 'ticker_historical': ticker_historical}
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