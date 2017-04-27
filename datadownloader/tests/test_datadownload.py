# -*- coding: utf-8 -*-

import pytest
import os.path
import tempfile
import shutil
try:
    from unittest import mock
except ImportError:
    import mock

from datadownloader.management.commands.datadownload import Command


@pytest.fixture(scope='session')
def temp_media():
    media_root = tempfile.mkdtemp()
    yield media_root
    shutil.rmtree(media_root)


@pytest.fixture
def media_root(temp_media, settings):
    settings.MEDIA_ROOT = temp_media


@pytest.fixture
def mock_requests():
    mock_requests = mock.Mock()
    with open(os.path.join(os.path.dirname(__file__), 'dump.tar.gz'), 'rb') as archive:
        mock_requests.get.return_value = mock.Mock(
            status_code=200,
            content=archive.read(),
        )
    return mock_requests


@pytest.fixture
def cmd(mock_requests):
    return Command(requests=mock_requests)


@pytest.mark.usefixtures('media_root')
def test_datadownload(mock_requests, cmd, temp_media):
    with mock.patch('datadownloader.management.commands.datadownload.call_command') as cc:
        cmd.handle('https://example.org/blabla?token=abc')

    mock_requests.get.assert_called_once_with('https://example.org/blabla?token=abc')
    cc.assert_called_once_with('dr_load', manifest=mock.ANY)
    assert cc.mock_calls[0][2]['manifest'].endswith('/dumps/drdump.manifest')

    try:
        with open(os.path.join(temp_media, 'upload/image.png'), 'rb') as image:
            assert image.read() == b'abc\n'
    except OSError:
        pytest.fail('File %s has not been copied' % 'upload/image.png')


@pytest.mark.usefixtures('media_root')
def test_datadownload_create(mock_requests, cmd, temp_media):
    with mock.patch('datadownloader.management.commands.datadownload.call_command'):
        with mock.patch('datadownloader.management.commands.datadownload.get_random_string',
                        return_value='yUTPPBSuUcbG'):
            cmd.handle('https://example.org/')

    assert mock_requests.get.mock_calls == [
        mock.call('https://example.org/create/data/?token=yUTPPBSuUcbG:jzJ6lwqrX7hIwlHaYWVwNqsGIJw'),
        mock.call('https://example.org/download/data/?token=yUTPPBSuUcbG:jzJ6lwqrX7hIwlHaYWVwNqsGIJw'),
    ]
