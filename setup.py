from setuptools import setup, find_packages

setup(
    name='django-datadownloader',
    version=__import__('datadownloader').__version__,
    description=__import__('datadownloader').__doc__,
    long_description=u"\n".join((open('README.md').read(),
                                open('CHANGELOG.md').read())),
    author='Philippe Lafaye',
    author_email='lafaye@emencia.com',
    url='http://pypi.python.org/pypi/django-datadownloader',
    license='GNU Affero General Public License v3',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
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
    install_requires=[
        'Django>=1.7',
        'dr-dump>=0.2.5',
    ],
    include_package_data=True,
    zip_safe=False
)
