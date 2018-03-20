from django.shortcuts import render
from .models import *

def index(request):
    if request.method == 'GET':
        all_company = Company.objects.all()
        context = {'title':'index', 'all_company': all_company}
        return render(request, 'dot_app/index.html', context)