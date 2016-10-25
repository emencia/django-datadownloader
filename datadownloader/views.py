import os
import tarfile
from datetime import datetime
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings


def get_base_path():
    if hasattr(settings, 'DATA_DOWNLOADER_PATH'):
        base_path = settings.DATA_DOWNLOADER_PATH
    else:
        base_path = os.path.join(settings.BASE_DIR, 'project',
                                 'protected_medias', 'datas')
    return base_path


def get_archives_info():
    info = {}
    project_name = settings.BASE_DIR.split("/")[-1]
    base_path = get_base_path()
    for section in ["db", "media", "data"]:
        file_name = "%s_%s.tar.gz" % (project_name, section)
        path = os.path.join(base_path, file_name)
        if os.path.exists(path):
            infos = os.stat(path)
            date = datetime.fromtimestamp(int(infos.st_mtime))
            info["%s_info" % section] = {'date': date,
                                         'size': infos.st_size}
        else:
            info["%s_info" % section] = {'date': None, 'size': None}
    return info


def create_archive(data_type):
    folders = []
    base_path = get_base_path()
    project_name = settings.BASE_DIR.split("/")[-1]
    tar_name = "%s_%s.tar.gz" % (project_name, data_type)
    path = os.path.join(base_path, tar_name)
    if data_type == "db" or data_type == "data":
        folders.append("dumps")
    if data_type == "media" or data_type == "data":
        folders.append("project/media")
    with tarfile.open(tar_name, "w:gz") as tar:
        for folder in folders:
            tar.add(folder)
    os.rename(tar_name, path)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.serialize_context(context),
            **response_kwargs
        )

    def serialize_context(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        del context['view']
        return context


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    def get_context_data(self, **kwargs):
        context = super(DataDownloaderMainView,
                        self).get_context_data(**kwargs)
        context.update(get_archives_info())
        return context


class DataDownloaderCreateArchiveView(JSONResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(DataDownloaderCreateArchiveView,
                        self).get_context_data(**kwargs)
        create_archive(context['data_type'])
        info = get_archives_info()
        context.update(info)
        return context
