# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from .views import DataDownloaderMainView, DataDownloaderCreateArchiveView
from .views import DataDownloaderDeleteArchiveView
from .views import DataDownloaderDownloadArchiveView


urlpatterns = patterns(
    '',
    url(r'^/$', staff_member_required(DataDownloaderMainView.as_view()),
        name="datadownloader_index"),
    url(r'^/create/(?P<data_type>[^/]+)/$',
        staff_member_required(DataDownloaderCreateArchiveView.as_view()),
        name="create_archive"),
    url(r'^/delete/(?P<data_type>[^/]+)/$',
        staff_member_required(DataDownloaderDeleteArchiveView.as_view()),
        name="delete_archive"),
    url(r'^/download/(?P<data_type>[^/]+)/$',
        staff_member_required(DataDownloaderDownloadArchiveView.as_view()),
        name="download_archive")
)
