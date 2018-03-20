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
    context = {'ticker': ticker.lower(),'test': len(ticker_historical), 'ticker_historical': ticker_historical}
    return render(request, 'dot_app/historical.html', context)