# -*- coding: utf-8 -*-

import shutil
import tempfile
import tarfile
import io
import os.path

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

    def _get_url(self, url):
        try:
            import requests
        except ImportError:
            raise ImportError('Package requests is required to fetch remotes artifacts.')
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RuntimeError('Unexpected response {} when getting {}'.format(resp, url))
        return resp

    def _get_remote(self, url, components):
        if "?token" not in url:
            components = set(components.split('+'))
            content = None
            if 'db' in components and 'media' in components:
                content = 'data'
            elif 'db' in components:
                content = 'db'
            elif 'media' in components:
                content = 'media'
            archive_path = reverse('download_archive',
                                   kwargs={'data_type': content})
            create_path = reverse('create_archive',
                                  kwargs={'data_type': content})
            token = signer.sign(get_random_string())
            create_url = "%s%s?token=%s" % (url, create_path, token)
            resp = self._get_url(create_url)
            url = "%s%s?token=%s" % (url, archive_path, token)
        resp = self._get_url(url)
        return io.BytesIO(resp.content)

    def _get_local(self, filename):
        return open(filename, 'rb')

    def handle(self, url, **options):
        try:
            content = None
            if '://' in url and not url.startswith('file://'):
                content = self._get_remote(url,
                                           options['components'] or 'db+media')
            else:
                content = self._get_local(url)
            self._handle_archive(tarfile.open(fileobj=content, mode='r'),
                                 options['components'] or 'db+media')
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
        members = [m for m in archive.getmembers() if m.name.startswith('dumps/')]
        try:
            tmpdir = tempfile.mkdtemp(prefix='datadownloader')
            archive.extractall(tmpdir, members)
            call_command('dr_load', manifest=os.path.join(tmpdir, 'dumps/drdump.manifest'))
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
