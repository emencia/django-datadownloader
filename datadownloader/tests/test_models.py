# -*- coding: utf-8 -*-

import unittest
import datetime
import os

try:
    import mock
except ImportError:
    from unittest import mock

from datadownloader.models import Dump
from django.conf import settings


class TestDump(unittest.TestCase):
    def test_metadata_empty(self):
        dump = Dump('db')
        self.assertEqual(dump.get_metadata(), {'size': None, 'date': None})

    def test_metadata(self):
        expected_dump_path = os.path.join(settings.DATA_DOWNLOADER_PATH,
                                          'django-datadownloader_db.tar.gz')
        dump = Dump('db')

        with mock.patch('os.stat') as stat:
            stat.return_value = mock.Mock(
                st_mtime=1478598236,
                st_size=12345,
            )
            metadata = dump.get_metadata()

        stat.assert_called_once_with(expected_dump_path)
        self.assertEqual(metadata, {
            'size': 12345,
            'date': datetime.datetime(2016, 11, 8, 3, 43, 56),
        })

    def test_destroy(self):
        expected_dump_path = os.path.join(settings.DATA_DOWNLOADER_PATH,
                                          'django-datadownloader_db.tar.gz')
        dump = Dump('db')

        with mock.patch('os.remove') as remove:
            dump.destroy()

        remove.assert_called_once_with(expected_dump_path)

    def test_create(self):
        expected_dump_path = os.path.join(settings.DATA_DOWNLOADER_PATH,
                                          'django-datadownloader_data.tar.gz')
        db_dumper = mock.Mock(return_value=['/abc/'])
        dump = Dump('data', database_dumper=db_dumper)

        tf, shutil = mock.Mock(), mock.Mock()
        with mock.patch.multiple('datadownloader.models', tarfile=tf, shutil=shutil):
            tf.open = mock.MagicMock()
            with mock.patch('os.mkdir'):
                dump.create()

        db_dumper.assert_called_once_with()
        tf.assert_has_calls([
            mock.call.open(expected_dump_path, 'w:gz'),
            mock.call.open().__enter__(),
            mock.call.open().__enter__().add(settings.MEDIA_ROOT, 'medias'),
            mock.call.open().__enter__().add('/abc/', 'abc/'),
            mock.call.open().__exit__(None, None, None),
        ])
