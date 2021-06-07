# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def parse_requirements(requirements_txt):
    requirements = []
    try:
        with open(requirements_txt, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                if '://' in line:
                    continue
                if line.startswith('-'):
                    raise ValueError('Unexpected command {0} in {1}'.format(
                        line,
                        requirements_txt,
                    ))

                requirements.append(line)
        return requirements
    except IOError:
        return []


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
        'Framework :: Django',
        "Framework :: Django :: 1.7",
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
    zip_safe=False
)
