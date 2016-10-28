import os
import tarfile
import subprocess
from datetime import datetime
from sendfile import sendfile
from django.views.generic import View, TemplateView
from django.conf import settings
from django.shortcuts import redirect


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
    # be sure to be in project root folder
    os.chdir(settings.BASE_DIR)
    if data_type == "db" or data_type == "data":
        folders.append("dumps")
        dumps_path = os.path.join(settings.BASE_DIR, "dumps")
        if os.path.exists(dumps_path):
            for dump_file in os.listdir(dumps_path):
                os.remove(os.path.join(dumps_path, dump_file))
        else:
            os.makedirs(dumps_path)
        subprocess.check_output('bin/datadump')
    if data_type == "media" or data_type == "data":
        folders.append("project/media")
    with tarfile.open(path, "w:gz") as tar:
        for folder in folders:
            tar.add(folder)


def delete_archive(data_type):
    base_path = get_base_path()
    project_name = settings.BASE_DIR.split("/")[-1]
    tar_name = "%s_%s.tar.gz" % (project_name, data_type)
    path = os.path.join(base_path, tar_name)
    os.remove(path)


class DataDownloaderMainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    def get_context_data(self, **kwargs):
        context = super(DataDownloaderMainView,
                        self).get_context_data(**kwargs)
        context.update(get_archives_info())
        return context


class DataDownloaderCreateArchiveView(View):
    def get(self, request, *args, **kwargs):
        create_archive(kwargs['data_type'])
        return redirect('datadownloader_index')


class DataDownloaderDeleteArchiveView(View):
    def get(self, request, *args, **kwargs):
        delete_archive(kwargs['data_type'])
        return redirect('datadownloader_index')


class DataDownloaderDownloadArchiveView(View):
    def get(self, request, *args, **kwargs):
        data_type = kwargs['data_type']
        base_path = get_base_path()
        project_name = settings.BASE_DIR.split("/")[-1]
        tar_name = "%s_%s.tar.gz" % (project_name, data_type)
        path = os.path.join(base_path, tar_name)
        return sendfile(request, path, attachment=True,
                        attachment_filename=tar_name)
