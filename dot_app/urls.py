# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.conf.urls import url

from .views import index, historical, insider, insider_name

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<ticker>[A-Za-z]+)$', historical, name="historical"),
    url(r'^(?P<ticker>[A-Za-z]+)/insider$', insider, name="insider"),
    url(r'^(?P<ticker>[A-Za-z]+)/insider/(?P<insider_name>[A-Za-z0-9 ]+)$', insider_name, name="insider_name"),

]