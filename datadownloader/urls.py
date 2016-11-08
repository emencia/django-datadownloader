# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    DataDownloaderMainView,
    DataDownloaderCreateArchiveView,
    DataDownloaderDeleteArchiveView,
    DataDownloaderDownloadArchiveView,
)


urlpatterns = [
    url(r'^$', DataDownloaderMainView.as_view(),
        name="datadownloader_index"),
    url(r'^create/(?P<data_type>(data|db|media))/$',
        DataDownloaderCreateArchiveView.as_view(),
        name="create_archive"),
    url(r'^delete/(?P<data_type>(data|db|media))/$',
        DataDownloaderDeleteArchiveView.as_view(),
        name="delete_archive"),
    url(r'^download/(?P<data_type>(data|db|media))/$',
        DataDownloaderDownloadArchiveView.as_view(),
        name="download_archive")
]
