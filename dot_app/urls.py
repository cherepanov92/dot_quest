# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.conf.urls import url

from .views import index, historical, insider

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<ticker>[A-Za-z]+)$', historical, name="historical"),
    url(r'^(?P<ticker>[A-Za-z]+)/insider$', insider, name="insider"),
]