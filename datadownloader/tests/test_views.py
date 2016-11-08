# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.test import TestCase, override_settings
from django.http import HttpResponse

from datadownloader.models import Dump

try:
    import mock
except ImportError:
    from unittest import mock


class AuthMiddleware(object):
    def process_request(self, req):
        req.user = mock.Mock()


@override_settings(
    MIDDLEWARE_CLASSES=[
        'datadownloader.tests.test_views.AuthMiddleware',
    ],
    ROOT_URLCONF='datadownloader.urls',
)
@mock.patch('datadownloader.views.Dump', spec=Dump)
class TestViews(TestCase):
    def test_main_view(self, Dump_):
        r = self.client.get('/')

        self.assertIsInstance(r, TemplateResponse)
        self.assertIn('token', r.context_data)
        self.assertEqual(r.context_data['metadata'], {
            'db': Dump_.return_value.get_metadata.return_value,
            'media': Dump_.return_value.get_metadata.return_value,
            'data': Dump_.return_value.get_metadata.return_value,
        })

    def test_create_view(self, Dump_):
        r = self.client.get('/create/data/', follow=False)
        self.assertEqual(r.status_code, 302)

        self.assertEqual(Dump_.mock_calls, [
            mock.call('data'),
            mock.call().create(),
        ])

    def test_destroy_view(self, Dump_):
        r = self.client.get('/delete/data/', follow=False)
        self.assertEqual(r.status_code, 302)

        self.assertEqual(Dump_.mock_calls, [
            mock.call('data'),
            mock.call().destroy(),
        ])

    def test_download_view(self, Dump_):
        r = self.client.get('/')
        token = r.context_data['token']

        Dump_.return_value.path = '/srv/123/x.tar.gz'
        with mock.patch('datadownloader.views.sendfile') as sendfile:
            sendfile.return_value = HttpResponse()
            r = self.client.get('/download/data/', data={'token': token}, follow=False)

        sendfile.assert_called_once_with(
            mock.ANY,
            '/srv/123/x.tar.gz',
            attachment=True,
            attachment_filename=Dump_.return_value.archive_name,
        )
