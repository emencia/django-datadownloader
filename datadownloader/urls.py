# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import DataDownloaderMainView, DataDownloaderCreateArchiveView


urlpatterns = patterns(
    '',
    url(r'^/$', DataDownloaderMainView.as_view()),
    url(r'^/create/(?P<data_type>[^/]+)/$',
        DataDownloaderCreateArchiveView.as_view(), name="create_archive")
)
