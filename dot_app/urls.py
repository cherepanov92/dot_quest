# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.conf.urls import url

from .views import  historical, insider, insider_name, analytics, delta

urlpatterns = [
    url(r'^$', historical, name="historical"),
    url(r'^insider$', insider, name="insider"),
    url(r'^insider/(?P<insider_name>[A-Za-z0-9 ]+)$', insider_name, name="insider_name"),
    url(r'^analytics$', analytics, name="analytics"),
    url(r'^delta$', delta, name="delta"),
]

# http://127.0.0.1:8000/goog/analytics/analytics?date_from=2018-01-22&date_to=2018-01-11