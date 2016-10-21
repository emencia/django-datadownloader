# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import DataDownloaderMainView


urlpatterns = patterns(
    '',
    url(r'^/$', DataDownloaderMainView.as_view()),
)
