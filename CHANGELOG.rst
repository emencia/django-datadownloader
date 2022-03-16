Changelog
=========

1.2.1 - 2022/03/16
------------------

Correct bug when DATA_DOWNLOADER_DUMP_PATH is not relative

1.2.0 - 2021/11/23
------------------

Add settings DATA_DOWNLOADER_DUMP_PATH for specify folder where drdump dumps
are stored

1.1.0 - 2021/06/08
------------------

Package now depends on "six" instead of using the deprecated embedded "six" module from
Django which are not available anymore since Django 3.0.

1.x will be the last serie to support Python 2 and Django<2.2 versions, new serie 2.x
will only support recent Python3 and Django versions.

Also did some cleaning in package setup and dependancies to fit to supported versions:

* six
* django>=1.8
* dr-dump>=1.1.0
* django-sendfile>=0.3.11


1.0.0 - 2018/09/26
------------------

Rewrite version.

Previously only release on a private package mirror, it have been release publicy to
official Pypi on 2021/06/07.

0.2.2
-----

* add some information into main page
* fix bug in uwsgi execution env

0.2.1
-----

* Forgot to update MANIFEST.in on 0.2.0 release

0.2.0
-----

* Refactoring code
* Adding tests

0.1.1
-----

* Use rst syntax for doc/descriptions rather markdown.

0.1.0
-----

* First version.
