# -*- coding: utf-8 -*-


import os
import sys
import shutil
import datetime
import subprocess
import tarfile

from django.conf import settings


def get_base_path():
    if hasattr(settings, 'DATA_DOWNLOADER_PATH'):
        base_path = settings.DATA_DOWNLOADER_PATH
    else:
        base_path = os.path.join(settings.BASE_DIR,
                                 'project/protected_medias/datas')
    return base_path


class Dump(object):
    def __init__(self, data_type, base_path=None):
        assert data_type in ('data', 'db', 'media')
        self.data_type = data_type
        self.base_path = base_path or get_base_path()

    def get_metadata(self):
        try:
            infos = os.stat(self.path)
            date = datetime.datetime.fromtimestamp(int(infos.st_mtime))
            return {
                'date': date,
                'size': infos.st_size
            }
        except OSError:
            return {
                'date': None,
                'size': None
            }

    @property
    def project_name(self):
        return os.path.basename(settings.BASE_DIR)

    @property
    def archive_name(self):
        return "%s_%s.tar.gz" % (self.project_name, self.data_type)

    @property
    def path(self):
        return os.path.join(self.base_path, self.archive_name)

    def _get_datadump_bin(self):
        if hasattr(settings, 'DATADUMP_BIN_PATH'):
            return settings.DATADUMP_BIN_PATH
        if hasattr(sys, 'real_prefix'):
            # Running in a virtual env
            candidate = os.path.join(sys.prefix, 'bin/datadump')
            if os.path.exists(candidate):
                return candidate

        # Try a globally installed instance
        return 'datadump'

    def _dump_media(self):
        return [settings.MEDIA_ROOT.replace("%s/" % os.getcwd(), ''), ]

    def _dump_db(self):
        self._clean_dumps_path()
        subprocess.check_output(self._get_datadump_bin())
        dump_path = os.path.join(settings.BASE_DIR, 'dumps')
        return [dump_path.replace("%s/" % os.getcwd(), ''), ]

    def _clean_dumps_path(self):
        dumps_path = os.path.join(settings.BASE_DIR, 'dumps')
        if os.path.exists(dumps_path):
            shutil.rmtree(dumps_path)
        os.mkdir(dumps_path)

    def create(self):
        folders = []
        if self.data_type == 'db':
            folders.extend(self._dump_db())
        elif self.data_type == 'media':
            folders.extend(self._dump_media())
        elif self.data_type == 'data':
            folders.extend(self._dump_media())
            folders.extend(self._dump_db())

        with tarfile.open(self.path, "w:gz") as tar:
            for folder in folders:
                tar.add(folder)

    def destroy(self):
        os.remove(self.path)
