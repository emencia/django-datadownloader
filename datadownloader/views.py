from django.views.generic import TemplateView


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"
