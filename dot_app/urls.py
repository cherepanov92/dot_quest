# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.conf.urls import url

from .views import  historical, insider, insider_name, analytics

urlpatterns = [
    url(r'^$', historical, name="historical"),
    url(r'^/insider$', insider, name="insider"),
    url(r'^/insider/(?P<insider_name>[A-Za-z0-9 ]+)$', insider_name, name="insider_name"),
]