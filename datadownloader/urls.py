# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    MainView,
    CreateArchiveView,
    DeleteArchiveView,
    DownloadArchiveView,
)


urlpatterns = [
    url(r'^$', MainView.as_view(),
        name="datadownloader_index"),
    url(r'^create/(?P<data_type>(data|db|media))/$',
        CreateArchiveView.as_view(),
        name="create_archive"),
    url(r'^delete/(?P<data_type>(data|db|media))/$',
        DeleteArchiveView.as_view(),
        name="delete_archive"),
    url(r'^download/(?P<data_type>(data|db|media))/$',
        DownloadArchiveView.as_view(),
        name="download_archive")
]
