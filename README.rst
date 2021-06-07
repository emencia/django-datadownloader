=====================
django-datadownloader
=====================

Description
***********

This django app is an app tool that add an admin interface for manage archives
of database's json dumps and/or media datas.

For the moment, this app use the script build by the
`emencia-recipe-drdump <https://pypi.python.org/pypi/emencia-recipe-drdump>`_
package (we must improve it for directly use
`dr-dump <https://github.com/emencia/dr-dump>`_ package.

Packages can be download with
`django-sendfile <https://pypi.python.org/pypi/django-sendfile>`_.

Install
*******

You can retrieve it via pip: ::

    pip install django-datadownloader

You can add this to your requirements file: ::

    django-datadownloader==1.0.0b5
    dr-dump==1.0.0b7

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
found inside datadownloader.tests.settings.

    $ django-admin test --pythonpath=. --settings=datadownloader.tests.settings

You must install mock if you run python2 or python < 3.4.
