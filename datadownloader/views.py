# -*- coding: utf-8 -*-

from sendfile import sendfile

from django.views.generic import View, TemplateView
from django.shortcuts import redirect

from datadownloader.models import Dump


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    def get_context_data(self, **kwargs):
        context = super(DataDownloaderMainView,
                        self).get_context_data(**kwargs)

        context['metadata'] = metadata = {}
        for section in ["db", "media", "data"]:
            dump = Dump(section)
            context['metadata'][section] = dump.get_metadata()
        return context


class DataDownloaderCreateArchiveView(View):
    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.create()
        return redirect('datadownloader_index')


class DataDownloaderDeleteArchiveView(View):
    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.destroy()
        return redirect('datadownloader_index')


class DataDownloaderDownloadArchiveView(View):
    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        return sendfile(request,
                        dump.path,
                        attachment=True,
                        attachment_filename=tar_name)
