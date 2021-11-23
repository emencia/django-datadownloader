# -*- coding: utf-8 -*-


import os
import sys
import shutil
import datetime
import subprocess
import tarfile
import drdump

from django.core.management import call_command
from django.conf import settings


def get_base_path():
    if hasattr(settings, 'DATA_DOWNLOADER_PATH'):
        base_path = settings.DATA_DOWNLOADER_PATH
    else:
        base_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'project/protected_medias/datas'))
    return base_path


class Dump(object):
    def __init__(self, data_type, base_path=None, database_dumper=None):
        assert data_type in ('data', 'db', 'media')
        self.data_type = data_type
        self.base_path = base_path or get_base_path()
        self.database_dumper = database_dumper or get_default_dumper()

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
    def mimetype(self):
        return "application/x-gzip"

    @property
    def path(self):
        return os.path.join(self.base_path, self.archive_name)

    def _dump_media(self):
        return [
            settings.MEDIA_ROOT,
        ]

    def _clean_dumps_path(self):
        dumps_path = os.path.join(settings.BASE_DIR, 'dumps')
        if os.path.exists(dumps_path):
            shutil.rmtree(dumps_path)
        os.mkdir(dumps_path)

    def _ensure_base_path(self):
        try:
            os.makedirs(self.base_path)
        except OSError:
            pass

    def create(self):
        folders = []
        if self.data_type == 'db':
            folders.extend(self.database_dumper())
        elif self.data_type == 'media':
            folders.extend(self._dump_media())
        elif self.data_type == 'data':
            folders.extend(self._dump_media())
            folders.extend(self.database_dumper())

        self._ensure_base_path()
        with tarfile.open(self.path, "w:gz") as tar:
            for folder in folders:
                archive_name = folder.replace(settings.BASE_DIR, '').lstrip('/')
                tar.add(folder, archive_name)

    def destroy(self):
        os.remove(self.path)


class OldDrDump(object):
    @classmethod
    def default(cls):
        if hasattr(settings, 'DATADUMP_BIN_PATH'):
            return cls(settings.DATADUMP_BIN_PATH)
        if hasattr(sys, 'real_prefix'):
            # Running in a virtual env
            candidate = os.path.join(sys.prefix, 'bin/datadump')
            if os.path.exists(candidate):
                return cls(candidate)

        # Try a globally installed instance
        return cls('datadump')

    def __init__(self, bin_path):
        self.bin_path = bin_path

    def __call__(self):
        self._clean_dumps_path()
        subprocess.check_output(self.bin_path)
        dump_path = os.path.join(settings.BASE_DIR, 'dumps')
        return [
            dump_path,
        ]


class DrDump(object):
    def __call__(self):
        dump_path = getattr(settings, 'DATA_DOWNLOADER_DUMP_PATH', 'dumps')
        call_command('dr_dump', '-o', 'dump_dir=%s' % dump_path)
        return [
            dump_path.replace("%s/" % os.getcwd(), ''),
        ]


if drdump.__version__.startswith('0.'):
    get_default_dumper = OldDrDump.default
else:
    get_default_dumper = DrDump
