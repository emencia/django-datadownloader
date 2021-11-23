# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='django-datadownloader',
    version=__import__('datadownloader').__version__,
    description=__import__('datadownloader').__doc__,
    long_description=u"\n".join((open('README.rst').read(),
                                open('CHANGELOG.rst').read())),
    long_description_content_type="text/x-rst",
    author='Philippe Lafaye',
    author_email='lafaye@emencia.com',
    url='http://pypi.python.org/pypi/django-datadownloader',
    license='GNU Affero General Public License v3',
    packages=find_packages(exclude=[
        'datadownloader.tests',
        'datadownloader.tests.*'
    ]),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        "six",
        "django>=1.8",
        "dr-dump>=1.1.5",
        "django-sendfile>=0.3.11",
    ],
    include_package_data=True,
    zip_safe=False
)
