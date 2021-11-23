=====================
django-datadownloader
=====================

Description
***********

This django app is an app tool that add an admin interface to manage archives
of database's json dumps and/or media datas.

Packages can be download with
`django-sendfile <https://pypi.python.org/pypi/django-sendfile>`_.

Install
*******

You can retrieve it via pip: ::

    pip install django-datadownloader

Usage
*****

You need to add two libraries in your ``INSTALLED_APPS``: ::

    INSTALLED_APPS = (
        ...
        'drdump',
        'datadownloader',
        ...
    )

Add this to your URLs: ::

    urlpatterns = [
        ...
        url(r'^admin/datadownloader/', include('datadownloader.urls')),
        ...
    ]

You can add a few options: ::

    DATA_DOWNLOADER_PATH = join(VAR_PATH, 'protected_medias/datas')
    DATA_DOWNLOADER_DUMP_PATH = join(VAR_PATH, 'dumps')
    DRDUMP_OTHER_APPS = True
    DRDUMP_MAP_FILE = join(BASE_DIR, 'drdump.json')
    DRDUMP_EXCLUDE_APPS = ['auth', 'sessions', 'contenttypes']

See DrDump documentation for more: https://github.com/emencia/dr-dump

Links
*****

* Pypi page: https://pypi.python.org/pypi/django-datadownloader
* Github page: https://github.com/emencia/django-datadownloader


Running tests
*************

To run the tests, run the django test management command with the settings
found inside ``datadownloader.tests.settings``: ::

    $ django-admin test --pythonpath=. --settings=datadownloader.tests.settings

You must install mock if you run python2 or python < 3.4.
