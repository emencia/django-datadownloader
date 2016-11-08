=====================
django-datadownloader
=====================

Description
===========

This django app is an app tool that add an admin interface for manage archives
of database's json dumps and/or media datas.

For the moment, this app use the script build by the
`emencia-recipe-drdump <https://pypi.python.org/pypi/emencia-recipe-drdump>`_
package (we must improve it for directly use
`dr-dump <https://github.com/emencia/dr-dump>`_ package.

Packages can be download with
`django-sendfile <https://pypi.python.org/pypi/django-sendfile>`_.

Links
=====

* Pypi page: https://pypi.python.org/pypi/django-datadownloader
* Github page: https://github.com/emencia/django-datadownloader


Running tests
=============

To run the tests, run the django test management command with the settings
found inside datadownloader.tests.settings.

    $ django-admin test --pythonpath=. --settings=datadownloader.tests.settings

You must install mock if you run python2 or python < 3.4.
