# -*- coding: utf-8 -*-

from sendfile import sendfile

from django.views.generic import View, TemplateView
from django.core.signing import Signer
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.http import HttpResponseForbidden

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required


signer = Signer(salt='datadownloader')

from datadownloader.models import Dump


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(DataDownloaderMainView, self).dispatch(*args, **kw)

    def get_context_data(self, **kwargs):
        context = super(DataDownloaderMainView,
                        self).get_context_data(**kwargs)

        context['token'] = signer.sign(get_random_string())
        context['metadata'] = metadata = {}
        for section in ["db", "media", "data"]:
            dump = Dump(section)
            context['metadata'][section] = dump.get_metadata()
        return context


class DataDownloaderCreateArchiveView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(DataDownloaderCreateArchiveView, self).dispatch(*args, **kw)

    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.create()
        return redirect('datadownloader_index')


class DataDownloaderDeleteArchiveView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(DataDownloaderDeleteArchiveView, self).dispatch(*args, **kw)

    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.destroy()
        return redirect('datadownloader_index')


class DataDownloaderDownloadArchiveView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            signer.unsign(token)
        except signing.BadSignature:
            return HttpResponseForbidden()

        dump = Dump(kwargs['data_type'])
        return sendfile(request,
                        dump.path,
                        attachment=True,
                        attachment_filename=tar_name)
