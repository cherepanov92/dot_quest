# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    # url(r'^form/', MyView.as_view(), name='form'),
]