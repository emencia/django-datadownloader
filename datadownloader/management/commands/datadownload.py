# -*- coding: utf-8 -*-
import shutil
import tempfile
import tarfile
import io
import os.path

from six.moves.urllib_parse import parse_qs, urlparse, urlunparse

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import signing
from django.utils.crypto import get_random_string

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

signer = signing.Signer(salt='datadownloader')


class Command(BaseCommand):
    def __init__(self, *args, **kw):
        self._requests = kw.pop('requests', None)
        super(Command, self).__init__(*args, **kw)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--media-only',
            action='store_const',
            const='media',
            dest='components',
            default='media+db'
        )
        parser.add_argument(
            '--db-only',
            action='store_const',
            const='db',
            dest='components',
        )
        parser.add_argument(
            'url'
        )

    @property
    def requests(self):
        if self._requests:
            return self._requests
        try:
            self._requests = __import__('requests')
        except ImportError:
            raise ImportError('Package requests is required to fetch remotes artifacts.')
        return self._requests

    def _get_url(self, url, params=None):
        resp = self.requests.get(url)
        if resp.status_code != 200:
            raise RuntimeError('Unexpected response {} when getting {}'.format(resp, url))
        return resp

    def _get_remote(self, url, components):
        parsed_url = urlparse(url)
        if 'token' not in parse_qs(parsed_url.query):
            components = set(components.split('+')) & {'db', 'media'}
            content = 'data' if components == {'db', 'media'} else components.pop()

            create_path = reverse('create_archive', kwargs={'data_type': content})
            token = signer.sign(get_random_string())
            query = 'token={}{}'.format(token, '&' + parsed_url.query if parsed_url.query else '')
            create_url = urlunparse([parsed_url.scheme, parsed_url.netloc, create_path, '', query, ''])
            resp = self._get_url(create_url)

            archive_path = reverse('download_archive', kwargs={'data_type': content})
            url = urlunparse([parsed_url.scheme, parsed_url.netloc, archive_path, '', query, ''])

        resp = self._get_url(url, params={'token': ''})
        return io.BytesIO(resp.content)

    def _get_local(self, filename):
        return open(filename, 'rb')

    def handle(self, url, **options):
        components = options.get('components') or 'db+media'
        try:
            content = None
            if '://' in url and not url.startswith('file://'):
                content = self._get_remote(url, components)
            else:
                content = self._get_local(url)
            self._handle_archive(tarfile.open(fileobj=content, mode='r'), components)
        finally:
            if content:
                content.close()

    def _handle_archive(self, archive, components):
        components = set(components.split('+'))
        if 'db' in components:
            self._load_db(archive)
        if 'media' in components:
            self._load_media(archive)

    def _load_db(self, archive):
        dump_path = getattr(settings, 'DATA_DOWNLOADER_DUMP_PATH', 'dumps')
        if dump_path.startswith('/'):
            dump_path = os.path.join(*dump_path.split(os.sep)[2:])
        members = [m for m in archive.getmembers() if m.name.startswith(dump_path)]
        try:
            tmpdir = tempfile.mkdtemp(prefix='datadownloader')
            archive.extractall(tmpdir, members)
            call_command('dr_load', manifest=os.path.join(tmpdir, dump_path,
                                                          'drdump.manifest'))
        finally:
            shutil.rmtree(tmpdir)

    def _load_media(self, archive):
        members = [m for m in archive.getmembers() if m.name.startswith('var/media')]
        for m in members:
            if os.path.basename(m.name).startswith('.'):
                continue
            target_path = m.name.replace('var/media', settings.MEDIA_ROOT)

            try:
                os.makedirs(os.path.dirname(target_path))
            except OSError as e:
                if e.errno != 17:  # File exists
                    raise

            file_content = archive.extractfile(m)
            if file_content is None:
                continue
            with open(target_path, 'wb') as target:
                target.write(file_content.read())
