import os
from datetime import datetime
from django.views.generic import TemplateView
from django.conf import settings


def get_archives_info():
    info = {}
    project_name = settings.BASE_DIR.split("/")[-1]
    if hasattr(settings, 'DATA_DOWNLOADER_PATH'):
        base_path = settings.DATA_DOWNLOADER_PATH
    else:
        base_path = os.path.join(settings.BASE_DIR, 'project',
                                 'protected_medias', 'datas')
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


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    def get_context_data(self, **kwargs):
        context = super(DataDownloaderMainView,
                        self).get_context_data(**kwargs)
        context.update(get_archives_info())
        return context
